import json
from Entities.ContextManager import ContextManager
import geojson


class TrafficViolation(ContextManager) :
    
    def __init__(self):
        super().__init__("","TrafficViolation") 
        self.location = geojson.Polygon(coordinates=[[geojson.Point(coordinates=[1,1]),geojson.Point(coordinates=[1,1]),geojson.Point(coordinates=[1,1]),geojson.Point(coordinates=[1,1])]])
        self.descr = "Description"
        self.seeAlso = [] # ref to onStreetParking

    def getRefOnStreetParking(self):
        return self.seeAlso

    def setLocationFromPoints(self,x1,y1,x2,y2):
        #self.location = geojson.Point(coordinates=[[(x1 + x2) / 2, (y1 + y2) / 2 ]]) # this is the location in the frame
        self.location = geojson.Polygon(coordinates=[[geojson.Point(coordinates=[1,1]),geojson.Point(coordinates=[1,1]),geojson.Point(coordinates=[1,1]),geojson.Point(coordinates=[1,1])]])

    
    def getDictObj(self):
        jsString = { 
                "id": self.id,
                "type" : self.type,
                "location": {
                    "value": self.location, 
                    "type": "GeoProperty"
                    },
                "description": {
                    "type": "String",
                    "value" : self.descr
                    },
                "seeAlso": {
                    "value" : self.seeAlso, 
                    "type" : "array"
                    }
            }
        return jsString
    
    def getLocation(self):
        jsString = { 
                "location": {
                    "value": self.location, 
                    "type": "GeoProperty"
                    },
            }
        return jsString
    
    def getDescription(self):
        jsString = { 
                "description": {
                    "type": "String",
                    "value" : self.descr
                    },
            }
        return jsString
    
    def getParkingSite(self):
        jsString = { 
                "seeAlso": {
                    "value" : self.seeAlso, 
                    "type" : "array"
                    }
            }
        return jsString
