import json
from Entities.ContextManager import ContextManager
import geojson

#status = (closed, free, occupied, unknown)

class ParkingSpot(ContextManager) :
    
    def __init__(self):
        super().__init__("","ParkingSpot") 
        self.location = geojson.Polygon(coordinates=[[geojson.Point(coordinates=[1,1]),geojson.Point(coordinates=[1,1]),geojson.Point(coordinates=[1,1]),geojson.Point(coordinates=[1,1])]])
        self.categ = "OnStreet"
        self.status = ["free"]
        self.refParkingSite = []

    def getDictObj(self):
        jsString = { 
                "id": self.id,
                "type" : self.type,
                "location": {
                    "value": self.location, 
                    "type": "GeoProperty"
                    },
                "category": {
                    "type": "array",
                    "value" : self.categ
                    },
                "status": {
                    "type": "String",
                    "value" : self.status
                    },                
                "refParkingSite": {
                    "value" : self.refParkingSite,
                    "type" : "array"
                    }
            }
       # print(json.dumps(jsString, indent=4))
        return jsString
   
   
obj = ParkingSpot()
obj.id = "ParkingSpot1"

#obj.setData(obj.getDictObj())
#obj.doPost()