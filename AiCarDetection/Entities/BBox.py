import supervision as sv
from Entities.BBox import BBox

class BBox():
    def __init__(self,bbox_list: sv.Detections, tracker_id : int):
        self.bbox = self.get_bbox_from_list(bbox_list,tracker_id=self.tracker_id)
        self.tracker_id = tracker_id
        self.xyxy = self.bbox[0]
    
    def getBBox(self):
        return self.bbox    
    
    def getTrackerId(self):
        return self.tracker_id
    
    def getXyxy(self):
        return self.xyxy
        
    def get_bbox_from_list(self, list_bbox, tracker_id):
        for bbox in list_bbox:
            if bbox[4] != None and bbox[4] == tracker_id:
                return bbox
        return None       
    
    def is_stationary(self, previous_bbox : BBox, threshold):
        parked = []
        tracker_id = previous_bbox.getTrckerId()
        previous_pos = previous_bbox.getXyxy()
        curr_i = self.get_bbox_from_list(tracker_id)
        motion_speed = threshold
        if curr_i :
            current_pos = curr_i[0]
            motion_speed = abs(current_pos[0] - previous_pos[0]) + abs(current_pos[1] - previous_pos[1])
        if motion_speed < threshold:
            parked.append(True)
        else:
            parked.append(False)

        return parked