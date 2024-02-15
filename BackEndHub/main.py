from typing import Union
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import Request, Depends,HTTPException
from sse_starlette.sse import EventSourceResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from app.Services.MainService import MainService
import logging
import asyncio
import json
import sys

from random import randint

class SSEManager:
    def __init__(self):
        self.subscriptions = []

    def add_subscription(self, response):
        self.subscriptions.append(response)

    def remove_subscription(self, response):
        self.subscriptions.remove(response)

    async def broadcast_message(self, message: dict):
        for response in self.subscriptions:
            await response.send_text(f"data: {json.dumps(message)}\n\n")

class TrafficViolation(BaseModel):
    tf_id: str
    tf_type: str
    description: str | None = None
    location: list | None = None
    is_resolved: float | None = None


sse_manager = SSEManager()
app = FastAPI()

STREAM_DELAY = 10  # second
RETRY_TIMEOUT = 15000  # milisecond
cnt = 0
data_to_be_sent = None

list_of_data_to_be_sent = []

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

fake_coordinates = [[38.248736, 21.738931], [38.246637, 21.736243], [38.247328, 21.737185]]

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.info('API is starting up')

async def get_body(request: Request):
    return await request.body()


@app.get("/getAllTrafficViolation")
def getDataFromDb():
    ms = MainService()
    list_records = ms.getTrafficViolationList() 
    logger.debug(list_records)
    return {'TrafficViolationList' : list_records}

@app.get("/getAllUnresolvedTrafficViolation")
def getDataFromDb2():
    ms = MainService()
    list_records = ms.getTrafficViolationListUnresolved() 
    logger.debug(list_records)
    return {'TrafficViolationList' : list_records}

@app.get("/getStats")
def getDataFromDb2():
    ms = MainService()
    list_records = ms.getTrafficViolationStats() 
    logger.debug(list_records)
    return {'TrafficViolationStats' : list_records}

@app.get("/getAllTParkingSites")
def getDataFromDb():
    ms = MainService()
    list_records = ms.getParkingSiteList() 
    logger.debug(list_records)
    return {'ParkingSiteList' : list_records}

@app.post("/updateResolved")
def updateTFResolved(tf : TrafficViolation):
    ms = MainService()
    ms.updateTFResolved(tf.tf_id, tf.is_resolved) 
    logger.debug(tf)
    return tf

@app.post("/notify")
def getDataFromContextBroker(body: bytes = Depends(get_body)):
    global data_to_be_sent, list_of_data_to_be_sent
    data_to_be_sent = body.decode('utf8')
    list_of_data_to_be_sent.append(data_to_be_sent)
    logger.info(data_to_be_sent)
    ms = MainService()
    data_to_insert = json.loads(data_to_be_sent)['data']
    data_to_insert = data_to_insert[0]
    logger.debug(data_to_insert)
    if data_to_insert['type'] == 'TrafficViolation':
        try:
            ms.insertTrafficViolation(data_to_insert['id'], data_to_insert['description']['value'],json.dumps(data_to_insert['location']['value']['coordinates']), json.dumps(data_to_insert['seeAlso']['value'][0]))
        except Exception as e:
            print(e)
            #TODO: maybe do something later...
    if data_to_insert['type'] == 'OnStreetParking':
        try:
            ms.insertOnStreetParking(data_to_insert['id'], data_to_insert['description']['value'],json.dumps(data_to_insert['location']['value']['coordinates']), json.dumps(data_to_insert['totalSpotNumber']['value']))
        except Exception as e:
            print(e)
            #TODO: maybe do something later...

    return body


async def sse_generator():
    global data_to_be_sent, cnt
    deb = False
    if deb is True:
        while True:
            num_items = randint(1, 3)  # Generate a random number of items
            values = []
            for _ in range(num_items):
                value={"id": "ID_"+str(randint(1000000000,9999999999)), "type": "TrafficViolation", "location": {"value": {"type": "Point", "coordinates": fake_coordinates[randint(0, len(fake_coordinates)-1)]}, "type": "GeoProperty"}, "description": {"type": "String", "value": "Illegal parking"}, "seeAlso": {"value": [], "type": "array"}}
                values.append(value)
            yield f"data: {json.dumps(values)}\n\n"
            await asyncio.sleep(randint(1, 5))     
    else:    
        while True:
            if len(list_of_data_to_be_sent) != 0 :
                item = list_of_data_to_be_sent.pop()
                if item is not None:
                    cnt = cnt + 1
                    #message = {'id': cnt,'data': 'data_body'}
                    #message['data'] = item
                    #yield f"data: {json.dumps(message)}\n\n"
                    item = json.loads(item)['data']
                    yield f"data: {json.dumps(item)}\n\n"
            await asyncio.sleep(1)
        # Adjust the sleep interval as needed
    
# Function to generate fake data
async def generate_fake_data():
    while True:
        num_items = randint(1, 3)  # Generate a random number of items
        values = []
        for _ in range(num_items):
            value={"id": "ID_"+str(randint(1000000000,9999999999)), "type": "TrafficViolation", "location": {"value": {"type": "Point", "coordinates": fake_coordinates[randint(0, len(fake_coordinates)-1)]}, "type": "GeoProperty"}, "description": {"type": "String", "value": "Illegal parking"}, "seeAlso": {"value": [], "type": "array"}}
            values.append(value)
        yield f"data: {json.dumps(values)}\n\n"
        await asyncio.sleep(randint(1, 5))  # Sleep for 1 second

# Define an endpoint to stream fake data
@app.get("/sseFake")
async def stream_fake_data(request: Request):
    async def fake_data_generator():
        async for item in generate_fake_data():
            yield item

    return StreamingResponse(fake_data_generator(), media_type="text/event-stream")


# when you want to run in on the host
"""
if __name__ == "__main__":
    uvicorn.run("main:app", port=5000, log_level="info")
"""    
@app.get("/sse", response_class=StreamingResponse)
async def sse_endpoint(request: Request):
    response = StreamingResponse(sse_generator(), media_type="text/event-stream")
    sse_manager.add_subscription(response)
    logger.info(len(sse_manager.subscriptions))
    return response