import json
from Entities.ContextManager import ContextManager
import geojson

class OnStreetParking(ContextManager) :
    
    def __init__(self):
        super().__init__("","OnStreetParking") 
        self.location = geojson.Polygon(coordinates=[[geojson.Point(coordinates=[1,1]),geojson.Point(coordinates=[1,1]),geojson.Point(coordinates=[1,1]),geojson.Point(coordinates=[1,1])]])
        self.totalSpotNumber = 0
        self.refParkingSpots = []
        self.seeAlso = []

    def getDictObj(self):
        jsString = { 
                "id": self.id,
                "type" : self.type,
                "location": {
                    "value": self.location, 
                    "type": "GeoProperty"
                    },
                "totalSpotNumber": {
                    "type": "Number",
                    "value" : self.totalSpotNumber
                    },
                "refParkingSpot": {
                    "value" : self.refParkingSpots,
                    "type" : "array"
                    },
                "seeAlso": {
                    "value" : self.seeAlso, 
                    "type" : "array"
                    }
            }
       # print(json.dumps(jsString, indent=4))
        return jsString
    def getRefTrafficViolation(self):
        return self.seeAlso
    def getTrafficViolationRef(self):
        jsString = { 
                "seeAlso": {
                    "value" : self.seeAlso, 
                    "type" : "array"
                    }
            }
        return jsString
