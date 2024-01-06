import os
from ultralytics import YOLO
from Entities.ParkingSpot import ParkingSpot
from Entities.TrafficViolation import TrafficViolation
from Entities.OnStreetParking import OnStreetParking

spot = ParkingSpot()
spot.id = "ParkingSpot2"
spot.setData(spot.getDictObj())
#spot.doPost()

obj = OnStreetParking()
obj.id = "ParkingSite2"
obj.refParkingSpots.append(spot.id)
obj.setData(obj.getDictObj())
spot.refParkingSite.append(obj.id)
#obj.doPost()

tv = TrafficViolation()
tv.id = "TrafficViolation2"
tv.seeAlso.append(obj.id)
tv.setData(tv.getDictObj())
#tv.doPost()
tv.descr = "Testing Description Update2..."
#tv.doPatch(tv.getDescription())
#tv.doDelete()
spot.doGet()
#model = YOLO("yolov8m.pt")
#results = model.track(source="AiCarDetection/input/demo.png", show=True, save=True) 
