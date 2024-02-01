from typing import Union
import uvicorn
from fastapi import FastAPI
from fastapi import Request, Depends,HTTPException
from sse_starlette.sse import EventSourceResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import logging
import sys
import asyncio
import json
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

sse_manager = SSEManager()
app = FastAPI()

STREAM_DELAY = 10  # second
RETRY_TIMEOUT = 15000  # milisecond
cnt = 0

data_to_be_sent = None

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.info('API is starting up')

# Function to generate fake data
async def generate_fake_data():
    while True:
        # Generate fake data (replace this with your actual data generation logic)
        value={"id": "ID_"+str(randint(1000000000,9999999999)), "type": "TrafficViolation", "location": {"value": {"type": "Point", "coordinates": [100, 100 ]}, "type": "GeoProperty"}, "description": {"type": "String", "value": "Illegal parking"}, "seeAlso": {"value": [], "type": "array"}}

        fake_item = {"data":[value]}
        yield f"data: {json.dumps(fake_item)}\n\n"
        await asyncio.sleep(randint(1, 10))  # Sleep for 1 second

# Define an endpoint to stream fake data
@app.get("/sseFake")
async def stream_fake_data(request: Request):
    async def fake_data_generator():
        async for item in generate_fake_data():
            yield item

    return StreamingResponse(fake_data_generator(), media_type="text/event-stream")


async def get_body(request: Request):
    return await request.body()


@app.post("/notify")
def getDataFromContextBroker(body: bytes = Depends(get_body)):
   global data_to_be_sent
   data_to_be_sent = body.decode('utf8')
   logger.info(data_to_be_sent)
   return body



async def sse_generator():
    global data_to_be_sent, cnt
    while True:
        if data_to_be_sent is not None:
            cnt = cnt + 1
            message = {'id': cnt,
                    'data': 'data_body'}
            message['data'] = data_to_be_sent
            data_to_be_sent = None
            yield f"data: {json.dumps(message)}\n\n"
        await asyncio.sleep(1)
    # Adjust the sleep interval as needed

@app.get("/sse", response_class=StreamingResponse)
async def sse_endpoint(request: Request):
    response = StreamingResponse(sse_generator(), media_type="text/event-stream")
    sse_manager.add_subscription(response)
    logger.info(len(sse_manager.subscriptions))
    return response




# when you want to run in on the host
if __name__ == "__main__": 
   uvicorn.run("main:app", port=5000, log_level="info")