import requests
import json

class ContextManager(object):
    def __init__(self, _id, _type):
        self.data = None
        self.id = _id
        self.type = _type
        self.response = None
        self.fiware_service = "patras_onstreetparking"
        self.fiware_service_path = "/"
        self.url = f"http://localhost:1026/v2/entities"
        self.header = {
        "Content-Type": "application/json",
        "Fiware-Service" : self.fiware_service ,
        "Fiware-ServicePath": self.fiware_service_path
        }
    def setData(self, data):
        self.data = data

    def getResponse(self):
        return self.response
    
    def doPost(self):
        try:
            self.response = requests.post(url=self.url, data=json.dumps(self.data), headers=self.header)
            print(self.response.content)
        except Exception as e:
            print(e)
        return self.response

    def doPut(self):
        try:
            self.response = requests.put(url=self.url, data=json.dumps(self.data), headers=self.header)
            print(self.response.content)
        except Exception as e:
            print(e)
        return self.response
        
    def doGet(self):
        getUrl = self.url + "/" + self.id
        getHeader = {
                "Fiware-Service" : self.fiware_service,
                "Fiware-ServicePath": self.fiware_service_path
            }
        try:
            self.response = requests.get(url=getUrl, headers=getHeader)
        except Exception as e:
            print(e)
        return self.response
        
    def doDelete(self):
        deleteUrl = self.url + "/" + self.id + "/"
        deleteHeader = {
                        "Fiware-Service" : self.fiware_service,
                        "Fiware-ServicePath": self.fiware_service_path
                    }
        try:
            self.response = requests.delete(url=deleteUrl, headers=deleteHeader)
        except Exception as e:
            print(e)
        return self.response

    def doPatch(self, attr):
        patchUrl = self.url +"/" + self.id + "/attrs/"
        try:
            self.response = requests.patch(url=patchUrl, data=json.dumps(attr), headers=self.header)
        except Exception as e:
            print(e)
        return self.response
