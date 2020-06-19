from fastapi import FastAPI, Request
from fastapi.logger import logger
from pydantic import BaseModel

app = FastAPI()


@app.put("/predict")
def get_prediction(request: Request):

    try:
        logger.info("+++++ REQUEST RECEIVED +++++")
        logger.info(f"CLIENT ADDRESS: {request.client.host}")
        logger.info(f"REQUEST METHOD: {request.method}")
        logger.info(f"REQUEST API: {request.url.path}")

        result = predict_module()
    except Exception as e:
        logger.exception("message")
        raise Exception(e)

    return result


def predict_module(input=None):
    return {"predict": "Cat", "Predict_probability": 0.67}
