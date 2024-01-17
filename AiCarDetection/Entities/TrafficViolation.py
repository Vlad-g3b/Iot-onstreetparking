import json
from Entities.ContextManager import ContextManager
import geojson
import random
from shapely.geometry import Polygon, Point
import random
# 1 Point 38.24345365877684, 21.732097598848988
# 2 Point 38.24343838611503, 21.732119727073147
# 3 Point 38.24396843560099, 21.73279791804642
# 4 Point 38.24398974043434, 21.732766772558346

class TrafficViolation(ContextManager) :
    
    def __init__(self):
        super().__init__("","TrafficViolation") 
        self.location = geojson.Polygon(coordinates=[[geojson.Point(coordinates=[1,1]),geojson.Point(coordinates=[1,1]),geojson.Point(coordinates=[1,1]),geojson.Point(coordinates=[1,1])]])
        self.descr = "Description"
        self.seeAlso = [] # ref to onStreetParking

    def getRefOnStreetParking(self):
        return self.seeAlso
    
    def generate_random_point_in_polygon(self, p1, p2, p3, p4, precision=10):
        polygon = Polygon([p1, p2, p3, p4])

        min_x, min_y, max_x, max_y = polygon.bounds

        while True:
            random_x = round(random.uniform(min_x, max_x), precision)
            random_y = round(random.uniform(min_y, max_y), precision)

            if self.is_point_inside_polygon(random_x, random_y, polygon):
                return random_x, random_y

    def is_point_inside_polygon(self,x, y, polygon):
        point = Point(x, y)
        return point.within(polygon)
    
    def setLocationFromPoints(self,x1,y1,x2,y2):
        # this is the location in the frame
        polygon = [
                    (38.243453, 21.732097),
                    (38.243438, 21.732119),
                    (38.243968, 21.732797),
                    (38.243989, 21.732766),
                    ]
        random_point = self.generate_random_point_in_polygon(polygon[0], polygon[1], polygon[2], polygon[3])
        self.location = {
                        "type": "Point", 
                        #"coordinates": [(x1 + x2)/2, (y1 + y2)/2 ]
                        "coordinates" : random_point
                        }
        #self.location = geojson.Polygon(coordinates=[[geojson.Point(coordinates=[1,1]),geojson.Point(coordinates=[1,1]),geojson.Point(coordinates=[1,1]),geojson.Point(coordinates=[1,1])]])

    
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
