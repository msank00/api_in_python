import json
import os
import time
import uuid

import redis 

from fastapi import FastAPI, File, HTTPException, Body
from starlette.requests import Request
from pydantic import BaseModel
from typing import List, Dict


# Connect to Redis server
REDIS_HOST="localhost" #os.environ.get("REDIS_HOST")
db = redis.StrictRedis(host=REDIS_HOST)

app = FastAPI()

CLIENT_SLEEP=0.25  # Time in ms between each poll by web server against Redis
CLIENT_MAX_TRIES=100

IMAGE_QUEUE="image_queue"# os.environ.get("IMAGE_QUEUE")

class PredictionInput(BaseModel):
    input: List

@app.get("/")
def index():
    return "Hello World!"

@app.post("/predict")
def predict(request: Request, body: PredictionInput = Body(
    ...,
    example={
        "input": [{"input_text":"winter is coming"}]
    },
)):
    data = {"success": False}
    
    if request.method == "POST":
        
        content = body.input
        print(content)
        
        # Generate an ID for the classification then add the classification ID + image to the queue
        k = str(uuid.uuid4())
        d = {"id": k, "input_text": content[0]['input_text']}
        db.rpush(IMAGE_QUEUE, json.dumps(d))
        
        # Keep looping for CLIENT_MAX_TRIES times
        num_tries = 0
        
        while num_tries < CLIENT_MAX_TRIES:
            num_tries += 1

            # Attempt to grab the output predictions
            output = db.get(k)

            # Check to see if our model has classified the input image
            if output is not None:
                # Add the output predictions to our data dictionary so we can return it to the client
                output = output.decode("utf-8")
                data["predictions"] = json.loads(output)

                # Delete the result from the database and break from the polling loop
                db.delete(k)
                break
            
            # Sleep for a small amount to give the model a chance to classify the input image
            time.sleep(CLIENT_SLEEP)
            
            # Indicate that the request was a success
            data["success"] = True
            
        else:
            raise HTTPException(status_code=400, detail="Request failed after {} tries".format(CLIENT_MAX_TRIES))
    
    return data