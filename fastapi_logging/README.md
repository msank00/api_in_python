# Override Uvicorn Logger in FastAPI using Loguru

![image](https://miro.medium.com/max/700/1*yiY7rmgrbYD37TjC4s0SBw.png)

- Run the below command from this directory:

```py
uvicorn main:app --port 5008 --access-log
```

- Look [here](https://medium.com/1mgofficial/how-to-override-uvicorn-logger-in-fastapi-using-loguru-124133cdcd4e) for more details.


## Simple Approach:

- Look at fastapi issue [#1276](https://github.com/tiangolo/fastapi/issues/1276) and solution [gist](https://gist.github.com/Slyfoxy/a3e31cfcc1b19cba8e1b626276148c49)

### Display request information suing simple approach

```py
from starlette.requests import Request
from fastapi import FastAPI, Body, status
from custom_logger import init_logging

app = FastAPI()

logger = init_logging(filename="/path/to/logfile.log")

def show_status(request: Request):
    # add request type POST/GET as well...
    logger.info(f"Endpoint: {request.url.path}")
    logger.info(f"Client host: {request.client.host}")
    logger.info(f"Client port: {request.client.port}")
    logger.info(f"User agent: {request.headers.get('user-agent')}")
    logger.info(f"Response status: {status.HTTP_200_OK}")
    
@app.get("/")
def index(request: Request):
    logger.info(">>>>> Connection Established <<<<<")
    show_status(request)
    return {"Connection established!"}
```


----
