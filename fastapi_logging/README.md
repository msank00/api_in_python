# Override Uvicorn Logger in FastAPI using Loguru

![image](https://miro.medium.com/max/700/1*yiY7rmgrbYD37TjC4s0SBw.png)

- Run the below command from this directory:

```py
uvicorn main:app --port 5008 --access-log
```

- Look [here](https://medium.com/1mgofficial/how-to-override-uvicorn-logger-in-fastapi-using-loguru-124133cdcd4e) for more details.


## Simple Approach:

- Look at fastapi issue [#1276](https://github.com/tiangolo/fastapi/issues/1276) and solution [gist](https://gist.github.com/Slyfoxy/a3e31cfcc1b19cba8e1b626276148c49)

----
