 <img src="https://img.shields.io/badge/application-REST%20API-yellow.svg?style=flat-square" alt="application API">  <img src="https://img.shields.io/badge/Python-3.6-green.svg?style=flat-square" alt="made with Python"> <img src="https://img.shields.io/badge/package-Flask-blue.svg?style=flat" alt="made with flask">

# :rocket: Simple Python API for ML project

- This meta project consists of simple script which can be used to create machine learning API in python which includes
separate template for creating `preprocessing`, `training` and `prediction` API along with `logging` and `basic error` handling facility. 
- The preprocessing, training, prediction module consists of dummy code which you can fill as per your wish.

## :star: Package Information
+ `flask`: for creating api
+ `logging`: for capturing the log
+ `threading`: for creating asynchronous function call for preprocessing and training

## :dart: Main Scripts

+ The `predict_api.py` holds the actual code for prediciton module for the `/predict` api.
+ The `train_api.py` holds the code for preprocessing and training module for the apis `/preprocess` and `/train`
+ The `notify_api.py` under directory `/testdir` holds the dummy scipt for `/notify` api for implementing callback facility
+ The `statr.sh` scripts can be used to start all the server at one go

----

## :large_blue_diamond: Start Prediction server (`/predict` API):

  +  `python predict_api.py` OR
  +  `python predict_api.py -h` will give the options
     ```py
      python predict_api.py -h
      usage: predict_api.py [-h] [--optHost OPTHOST] [--optPort OPTPORT]
                          [--logLevel LOGLEVEL]

      Get Hosting parameters

      optional arguments:
        -h, --help           show this help message and exit
        --optHost OPTHOST    An optional Host Name
        --optPort OPTPORT    An optional port Number
        --logLevel LOGLEVEL  Logging level
     ```
     and you can run `python prediction_API.py --optPort=5000` or
  + use the `start.sh` file and run `./start.sh`

----

## :large_blue_diamond: Run client from terminal
  + Following curl command can be used:

```py
curl http://localhost:<port number>/predict --data '[{"UID":"1","AGE":"15"},{"UID":"2","AGE":"12"},{"UID":"3","AGE":"55"},{"UID":"4","AGE":"37"}]' -H "Content-Type: application/json" 
```

+ `/predict` is the prediction API end point
+ You may need to update the `port number` in the above curl command

----

## :large_blue_diamond: Start Training server (`/preprocess` and `/train` API):
  +  `python train_api.py` OR
  +  `python train_api.py -h` will give the options
     ```py
      python train_api.py -h
      usage: train_api.py [-h] [--optHost OPTHOST] [--optPort OPTPORT]
                          [--logLevel LOGLEVEL]

      Get Hosting parameters

      optional arguments:
        -h, --help           show this help message and exit
        --optHost OPTHOST    An optional Host Name
        --optPort OPTPORT    An optional port Number
        --logLevel LOGLEVEL  Logging level
     ```
     and you can run `python train_API.py --optPort=6000` or
  + use the `start.sh` file and run `./start.sh`

+ As training and preprocessing can take several minutes, they should be called asynchronously using python package `threading` followed by a post call to the `callback API` for sending the status of preprocessing and training.

----

## :large_blue_diamond: Run client from terminal 
  - curl for preprocessing api `/preprocess`

```py
curl http://localhost:<port number>/preprocess --data '{"callbackURL":"http://localhost:5020/notify"}' -H "Content-Type: application/json"
```
  - curl for training api `/train`

```py
curl http://localhost:<port number>/train --data '{"callbackURL":"http://localhost:5020/notify"}' -H "Content-Type: application/json"
```

  + The above `callbackURL` is a `notify api` for testing the async. The `notify api` script is in `/notify` folder. 
  + Run the nority callback API from _project main directory_ `python noitfy/notify_api.py`

----

# Swagger based api:

- Kindly look into the `swagger_api` folder

----

### :soon: TODO 

-  [x] Add `requirement.txt` file
-  [X] Implement with `fastapi` [click [here](https://github.com/tiangolo/fastapi)]
   -  [X] Add swagger UI
-  [ ] Add error code
-  [ ] Add simple web UI

----