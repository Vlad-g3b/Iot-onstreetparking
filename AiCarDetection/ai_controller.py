import cv2
import numpy as np
import supervision as sv
import ultralytics
import time
import calendar
import requests
from ultralytics import YOLO
from collections import defaultdict
from supervision.geometry.core import Position
from Entities.Car import Car
from Entities.ParkingSpot import ParkingSpot
from Entities.TrafficViolation import TrafficViolation
from Entities.OnStreetParking import OnStreetParking
from queue import Empty, Queue
from threading import Thread

dete = False
previous_bbox = None
parked = []
cars = {}
time_between_checks = 10
time_counter = 0


def get_bbox_from_list(list_bbox, tracker_id):
    for bbox in list_bbox:
        if bbox[4] != None and bbox[4] == tracker_id:
            return bbox
    return None

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

def consumer(queue):
    while True:
        try:
            item = queue.get()
        except Empty:
            continue
        else:
            print(f'Processing request item {item.getDictObj()}')
            response = item.doPost()
            time.sleep(12)
            queue.task_done()

def process_frame_tracking(frame: np.ndarray, time_elapsed) -> np.ndarray:
    # detect
    global previous_bbox ,time_counter, time_between_checks,parked, parking_site, queue
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
        session = requests.Session()
        session.headers.update(parking_site.header)
        notify = False
        for i in cars:
            if cars[i].car_parked is True:
                current_GMT = time.gmtime()
                time_stamp = calendar.timegm(current_GMT)
                print("Notify cygnus for car #{0} parked:{1} ".format(cars[i].car_id, cars[i].car_parked))
                tf = TrafficViolation()
                tf.id = "IllegalParking_" + str(cars[i].car_id) + "_" + str(parking_site.id) + "_" + str(time_stamp)# parking_site + timestamp to make it unique
                tf.descr = "illegal parking for atleast {0}".format(cars[i].time_stationary)
                #location in video
                tf.setLocationFromPoints(cars[i].car_position[0],cars[i].car_position[1],cars[i].car_position[2],cars[i].car_position[3])
                tf.getRefOnStreetParking().append(parking_site.id)
                tf.setData(tf.getDictObj())
                queue.put(tf)
                #response = tf.doPost()
                parking_site.getRefTrafficViolation().append(tf.id)
                notify=True
                list_to_pop.append(i)
                

        if notify:
            parking_site.setData(parking_site.getDictObj())
            response_site = parking_site.doPatch(parking_site.getTrafficViolationRef())
                
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
#polygon = np.array([
#    [290 , 80],
#    [255, 205],
#    [315, 205],
#    [340, 90],
#])
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
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
print('width:  ', width)
print('height: ', height)
parking_site = OnStreetParking()

current_GMT = time.gmtime()
time_stamp = calendar.timegm(current_GMT)
parking_site.id = "ParkingSite_" + str(time_stamp)
parking_site.description = "Street-Korinthou"
parking_site.setData(parking_site.getDictObj())
response = parking_site.doPost()
print(response)
#Create a queue for notifications
queue = Queue()
consumer_thread = Thread(target=consumer,args=(queue,),daemon=True)
consumer_thread.start()
# Loop through the video frames
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
queue.join()
# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()

from IPython import display
display.clear_output()