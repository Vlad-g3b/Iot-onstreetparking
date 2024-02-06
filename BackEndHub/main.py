from typing import Union
import uvicorn
from fastapi import FastAPI
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from app.Services.MainService import MainService
import logging
import asyncio
import json
from random import randint

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

@app.post("/notify")
def getDataFromContextBroker(body: bytes = Depends(get_body)):
    global data_to_be_sent, list_of_data_to_be_sent
    data_to_be_sent = body.decode('utf8')
    list_of_data_to_be_sent.append(data_to_be_sent)
    logger.debug("HERE")
    logger.info(data_to_be_sent)
    ms = MainService()
    data_to_insert = json.loads(data_to_be_sent)['data']
    logger.debug(data_to_insert)
    data_to_insert = data_to_insert[0]
    logger.debug(data_to_insert)
    if data_to_insert['type'] == 'TrafficViolation':
        try:
            ms.insertTrafficViolation(data_to_insert['id'], data_to_insert['description']['value'],json.dumps(data_to_insert['location']['value']), json.dumps(data_to_insert['seeAlso']['value'][0]))
        except Exception as e:
            print(e)
            #TODO: maybe do something later...

    return body


async def sse_generator():
    global data_to_be_sent, cnt
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
if __name__ == "__main__":
    uvicorn.run("main:app", port=5000, log_level="info")
    if len(list_of_data_to_be_sent) != 0 :
        item = list_of_data_to_be_sent.pop()
        if item is not None:
            cnt = cnt + 1
            message = {'id': cnt,
                    'data': 'data_body'}
            message['data'] = item
            yield f"data: {json.dumps(message)}\n\n"
    await asyncio.sleep(1)
    # Adjust the sleep interval as needed
    
@app.get("/sse", response_class=StreamingResponse)
async def sse_endpoint(request: Request):
    response = StreamingResponse(sse_generator(), media_type="text/event-stream")
    sse_manager.add_subscription(response)
    logger.info(len(sse_manager.subscriptions))
    return response