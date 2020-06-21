import uvicorn
import argparse
from fastapi import FastAPI, BackgroundTasks,  Request, Body
from fastapi.logger import logger
from pydantic import BaseModel
from typing import List, Dict
import json
import requests as req
import pandas as pd 
import random
import numpy as np
import time
from datetime import datetime
import calendar
import asyncio

class PredictionInput(BaseModel):
    input: List
    
class PreprocessInput(BaseModel):
    input: Dict

class TrainingInput(BaseModel):
    input: Dict

app = FastAPI(title="Generic ML API",
              description="This is a fancy project, with auto docs for the general Machine Learning API and everything",
              version="1.0.0",)


def get_unix_time():
    d = datetime.utcnow()
    unixtime = calendar.timegm(d.utctimetuple())
    return unixtime

def show_status(request: Request):
    logger.info("+++++ REQUEST RECEIVED +++++")
    logger.info(f"CLIENT ADDRESS: {request.client.host}")
    logger.info(f"REQUEST METHOD: {request.method}")
    logger.info(f"REQUEST API: {request.url.path}")
    logger.info(f"PORT: {request.url.port}") 



@app.put("/preprocess", tags=["Preprocessing"], summary="Preprocess the data")
async def preprocess_data(request: Request,  
                          background_tasks: BackgroundTasks,
                          body: PreprocessInput = Body(
    ...,
    example={
        "input": {"callbackURL":"http://localhost:5020/notify"}
    },
)):
    """
    Preprocess training data.
    
    Args:
    
    - Input type: Dict having a callbackURL    
    - **callbackURL**: url to post the notification after finishing the task
    """
    try:
        show_status(request)
        callback_url = body.input["callbackURL"]
        print(callback_url)
        background_tasks.add_task(preprocessing_module, callback_url)
    except Exception as e:
        raise Exception(e)

    return {"Status": "Preprocessing Started"}


# ==========original preprocessing module========
# .. here we have added a dumy for loop with sleep
# .. to simulate the time consuming algorithm and then
# .. we are making a callback to the given api
async def preprocessing_module(callbackURL:str):

    try:
        # ====================================================
        # all the preprocessing algorithm function calls goes here
        # ====================================================

        print("Inside Preprocessing Task...\nIt may take some time...")
        n = 10
        for i in range(1, n+1):
            # simulating as if each epoch is taking 
            # 5 seconds to complete
            print(f"Data chuck: {i}/{n}")
            await asyncio.sleep(5)

        logger.info("Preprocessing Successful")
        logger.info("POST status to callback API")

        task_type = "preprocess"
        status_message = "OK"
        unix_time = get_unix_time()

        # posting status to callback api
        post_status(callbackURL, status_message, task_type, unix_time)

        return

    except Exception as e:
        raise Exception(e)

def post_status(callback_url:str, status_msg:str, task: str, timestamp: int):
    """Post status to notification api acting as callback url

    Args:
        callback_url (str): URL to post notification
        status_msg (str): OK / NOTOK
        task (str): type of task: training/ preprocessing
        timestamp (int): timestamp of the task
    """

    callbackAddress = callback_url  #'http://localhost:5020/notify'
    task_type = task  # "preprocessing"
    status_message = status_msg  # "OK"
    unix_time = timestamp  # 1234

    payload_notify = {}
    payload_notify["task_type"] = task_type
    payload_notify["status_message"] = status_message
    payload_notify["unix_time"] = unix_time

    
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    response = req.post(
        callbackAddress, data=json.dumps(payload_notify), headers=headers
    )
    callbackAPIstatus = "callback api status code:" + str(response.status_code)
    print(callbackAPIstatus)
    logger.info(callbackAPIstatus)
    
    return


@app.put("/train", tags=["Training"], summary="Tran the model")
def train_model(request: Request, 
                background_tasks: BackgroundTasks,
                body: TrainingInput = Body(
    ...,
    example={
        "input": {"callbackURL":"http://localhost:5020/notify"}
    },
)):
    """
    Training model

    Args:
    
    - Input type: Dict having a callbackURL    
    - **callbackURL**: url to post the notification after finishing the task

    """
    try:
        show_status(request)
        callback_url = body.input["callbackURL"]
        print(callback_url)
        background_tasks.add_task(training_module, callback_url)
    except Exception as e:
        raise Exception(e)

    return {"Status": "Training Started"}


# ==========original training module========
# .. here we have added a dumy for loop with sleep
# .. to simulate the time consuming algorithm and then
# .. we are making a callback to the given api
async def training_module(callback_url:str):

    try:
        # ====================================================
        # all the training algorithm function calls goes here
        # ====================================================

        print("Inside Training Module...\nIt may take some time...")
        n = 10
        for i in range(1, n+1):
            # simulating as if each epoch is taking 
            # 5 seconds to complete
            print(f"Epoch: {i}/{n}")
            await asyncio.sleep(5)

        logger.info("Training Successful")
        logger.info("POST status to callback API")

        task_type = "training"
        status_message = "OK"
        unix_time = get_unix_time()

        print(task_type)
        print(status_message)
        print(unix_time)
        print(callback_url)

        # posting status to callback api
        post_status(callback_url, status_message, task_type, unix_time)

        return

    except Exception as e:
        app.logger.exception("message")
        raise Exception(e)


@app.put("/predict", tags=["Prediction"], summary="Get prediction from model")
def get_prediction(request: Request, body: PredictionInput = Body(
    ...,
    example={
        "input": [{"UID":"1","AGE":"15"},{"UID":"2","AGE":"12"}]
    },
)):
    """
    Generate prediction for `single input` or `bulk input`
    
    - Input type: List of json, where each json has    

    - **UID**: ID of the test input
    - **AGE**: Age of the item
    """

    try:
        logger.info("+++++ REQUEST RECEIVED +++++")
        logger.info(f"CLIENT ADDRESS: {request.client.host}")
        logger.info(f"REQUEST METHOD: {request.method}")
        logger.info(f"REQUEST API: {request.url.path}")
        logger.info(f"PORT: {request.url.port}") 

        print(f"Input body: {body.input}")
        
        content = json.dumps(body.input)
        df_content = pd.read_json(content, orient="records")
        
        # passing data to prediction module
        output = prediction_module(df_content)
        output_json = output.to_json(orient="records")
    except Exception as e:
        raise Exception(e)



    return output_json

@app.get("/model", tags=["Prediction"], summary="Get model file path")
def get_model(request: Request):
    show_status(request)
    return {"model_file": "path/to/model.bin"}

def prediction_module(input_data: pd.DataFrame):

    try:
        # ====================================================
        # all the prediction algorithm function calls goes here
        # ====================================================

        # dummy logic to get random prediction score
        n = input_data.shape[0]
        logger.info(f"Number of prediction input: {n}")

        df_pred = pd.DataFrame()
        df_pred["UID"] = input_data["UID"]
        df_pred["Prediction"] = random.choices(["dog","cat","monkey"], k=n)
        df_pred["Pred_Proba"] = np.random.uniform(0, 1, n)

        return df_pred
    except Exception as e:
        raise Exception(e)


