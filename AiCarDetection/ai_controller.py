import cv2
import numpy as np
import supervision as sv
import ultralytics
from ultralytics import YOLO
from collections import defaultdict
from supervision.geometry.core import Position
from Entities.Car import Car

dete = False
previous_bbox = None
stationary_threshold = 20
frame_count = 20
parked = []
cars = {}
time_between_checks = 10
time_counter = 0
def get_bbox_from_list(list_bbox, tracker_id):
    for bbox in list_bbox:
        if bbox[4] != None and bbox[4] == tracker_id:
            return bbox
    return None

def is_stationary(previous_bbox, current_bbox, threshold):
    parked = []
    for prev_i in previous_bbox:
        tracker_id = prev_i[4]
        previous_pos = prev_i[0]
        curr_i = get_bbox_from_list(current_bbox,tracker_id)
        motion_speed = threshold
        if curr_i :
            current_pos = curr_i[0]
            motion_speed = abs(current_pos[0] - previous_pos[0]) + abs(current_pos[1] - previous_pos[1])
        if motion_speed < threshold:
            print("is Stationary {0}".format(tracker_id))
            parked.append(True)
        else:
            parked.append(False)
    return parked

def update_cars(detections :sv.Detections, prev_detection : sv.Detections, time_elapsed):
    global cars
    parked = []
    for item in prev_detection:
        car = None
        tracker_id = item[4]
        if len(cars) > 0 and tracker_id in cars:
            car = cars[item[4]]
        else:
            car = Car()
        previous_pos = item[0]
        curr_i = get_bbox_from_list(detections, tracker_id)
        if curr_i:
            current_pos = curr_i[0]
            car.updateCar(tracker_id,previous_pos, current_pos, time_elapsed)
            cars[car.car_id] = car 
        parked.append(car.car_parked)
    return parked


def process_frame_tracking(frame: np.ndarray, time_elapsed) -> np.ndarray:
    # detect
    global previous_bbox ,time_counter, time_between_checks,parked
    results = model(frame,verbose=False)[0]
    detections = sv.Detections.from_ultralytics(results)
    #detections = detections[detections.class_id == 2]
    detections = tracker.update_with_detections(detections)
    current_parked = parked
    detection_zone_mask = zone.trigger(detections=detections)
    detection_zone_in = detections[detection_zone_mask]
    detections = detection_zone_in
    current_bbox = detections
    
    if len(current_parked) < len(detections):
        current_parked.extend([False] * (len(detections) - len(current_parked)))  # Extend list1 with zeros
    
    if previous_bbox :
        parked = update_cars(current_bbox, previous_bbox, time_elapsed)
    
    previous_bbox = current_bbox
    
    if time_counter == int(time_elapsed):
        print(" --Reset Frame Time Counter : ", str(time_counter))  
        time_counter = time_counter + time_between_checks
        #send a notification to cygnus when a car is found parked
        list_to_pop = []
        for i in cars:
            if cars[i].car_parked is True:
                print("Notify cygnus for car #{0} parked:{1} ".format(cars[i].car_id, cars[i].car_parked))
                #TODO define trafficViolation and push to context-broker
            list_to_pop.append(i)
        for i in list_to_pop:
            cars.pop(i)

    labels = []
    for class_id, tracker_id, parked_value in zip(detections.class_id, detections.tracker_id, current_parked):
        labels.append(f"#{tracker_id} {results.names[class_id]} #parked={parked_value}")
              
    annotated_frame = box_annotator.annotate(frame.copy(), detections=detections)
    annotated_frame = label_annotator.annotate(annotated_frame, detections=detections, labels=labels)
    annotated_frame = trace_annotator.annotate(annotated_frame, detections=detections)
    annotated_frame = zone_annotator.annotate(scene=annotated_frame)
    
    return annotated_frame


# initiate polygon zone
polygon = np.array([
    [290 , 80],
    [255, 205],
    [315, 205],
    [340, 90],
])
polygon = np.array([
    [522 , 202],
    [530, 703],
    [830, 595],
    [675, 180],
])
video_path = "AiCarDetection/input/video.mp4"
video_info = sv.VideoInfo.from_video_path(video_path)
zone = sv.PolygonZone(polygon=polygon, frame_resolution_wh=video_info.resolution_wh)
model = YOLO('yolov8n.pt')
# initiate annotators
zone_annotator = sv.PolygonZoneAnnotator(zone=zone, color=sv.Color.white())
tracker = sv.ByteTrack()
box_annotator = sv.BoundingBoxAnnotator()
label_annotator = sv.LabelAnnotator()
trace_annotator = sv.TraceAnnotator()
cap = cv2.VideoCapture(video_path)
# Loop through the video frames
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
print('width:  ', width)
print('height: ', height)
#TODO define ParkingSite and push to context-brocker

while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()
   # print(str(cap.get(cv2.CAP_PROP_POS_MSEC)/1000) + "\r")
    if success:
        annotated_frame = process_frame_tracking(frame=frame,time_elapsed=(cap.get(cv2.CAP_PROP_POS_MSEC)/1000))
        # Display the annotated frame
        cv2.imshow("YOLOv8 Tracking", annotated_frame)
        if dete:
            break
        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
        # Break the loop if 'q' is pressed

    else:
        # Break the loop if the end of the video is reached
        break

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()

from IPython import display
display.clear_output()