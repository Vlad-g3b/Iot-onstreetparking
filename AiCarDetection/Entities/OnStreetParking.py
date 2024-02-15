import json
from Entities.ContextManager import ContextManager
import geojson
# Google Maps coordinates
# 1 Point 38.24345365877684, 21.732097598848988
# 2 Point 38.24343838611503, 21.732119727073147
# 3 Point 38.24396843560099, 21.73279791804642
# 4 Point 38.24398974043434, 21.732766772558346
class OnStreetParking(ContextManager) :
    
    def __init__(self):
        super().__init__("","OnStreetParking") 
        self.location = geojson.Polygon(coordinates=[[geojson.Point(coordinates=[38.24345365877684, 21.732097598848988]),geojson.Point(coordinates=[38.24343838611503, 21.732119727073147]),geojson.Point(coordinates=[38.24396843560099, 21.73279791804642]),geojson.Point(coordinates=[38.24398974043434, 21.732766772558346])]])
        self.description = ""
        self.totalSpotNumber = 0
        self.refParkingSpots = []
        self.seeAlso = []

    def getDictObj(self):
        jsString = { 
                "id": self.id,
                "type" : self.type,
                "description": {
                    "type": "String",
                    "value" : self.description
                    },
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
