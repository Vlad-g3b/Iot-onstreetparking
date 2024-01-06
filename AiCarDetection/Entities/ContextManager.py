import requests
import json

class ContextManager(object):
    def __init__(self, id, type):
        self.data = None
        self.id = None
        self.type = None
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
        self.response = requests.post(url=self.url, data=json.dumps(self.data), headers=self.header)
        print(self.response.content)
        print(self.response)

    def doPut(self):
        raise Error("to be implemented!")
        self.response = requests.put(url=self.url, data=json.dumps(self.data), headers=self.header)
        print(self.response.content)
        
    def doGet(self):
        getUrl = self.url + "/" + self.id
        getHeader = {
                "Fiware-Service" : self.fiware_service,
                "Fiware-ServicePath": self.fiware_service_path
            }
        self.response = requests.get(url=getUrl, headers=getHeader)
        print(self.response.content)
        
    def doDelete(self):
        deleteUrl = self.url + "/" + self.id + "/"
        deleteHeader = {
                        "Fiware-Service" : self.fiware_service,
                        "Fiware-ServicePath": self.fiware_service_path
                    }
        self.response = requests.delete(url=deleteUrl, headers=deleteHeader)
        print(self.response.content)

    def doPatch(self, attr):
        patchUrl = self.url +"/" + self.id + "/attrs/"
        self.response = requests.patch(url=patchUrl, data=json.dumps(attr), headers=self.header)
        print(self.response.content)