from typing import Union
import uvicorn
from fastapi import FastAPI
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import logging
import asyncio
import json
from random import randint

app = FastAPI()

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