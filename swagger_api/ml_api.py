import uvicorn
import argparse
from fastapi import FastAPI, Request, Body
from fastapi.logger import logger
from pydantic import BaseModel
from typing import List, Dict
import json
import pandas as pd 
import random
import numpy as np

class PredictionInput(BaseModel):
    input: List

app = FastAPI(title="Generic ML API",
              description="This is a fancy project, with auto docs for the general Machine Learning API and everything",
              version="1.0.0",)



def show_status(request: Request):
    logger.info("+++++ REQUEST RECEIVED +++++")
    logger.info(f"CLIENT ADDRESS: {request.client.host}")
    logger.info(f"REQUEST METHOD: {request.method}")
    logger.info(f"REQUEST API: {request.url.path}")
    logger.info(f"PORT: {request.url.port}") 


@app.get("/preprocess", tags=["Preprocessing"], summary="Preprocess the data")
def get_prediction(request: Request):
    """
    Preprocess training data :rocket:
    """
    try:
        show_status(request)
        # call the preprocessing module here...
    except Exception as e:
        raise Exception(e)
    
    return {"Status": "Preprocessing Started"}


@app.get("/train", tags=["Training"], summary="Tran the model")
def get_prediction(request: Request):
    """
    Train the model :rocket:
    """
    try:
        show_status(request)
        # call the training module here
            
    except Exception as e:
        raise Exception(e)

    
    return {"Status": "Training Started"}


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


