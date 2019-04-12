# Sample API in PYTHON
This meta project consists of sample script which can be used to create machine learning API in python which includes
separate template for creating `preprocessing`, `training` and `prediction` API along with logging and basic error handling facility. 

# Package Information
+ package `flask`: for creating api
+ package `logging`: for capturing the log
+ package `threading`: for creating asynchronous function call for preprocessing and training

# Main Scripts

+ The `predict_API.py` holds the actual code for prediciton module for the `/predict` api.
+ The `train_API.py` holds the code for preprocessing and training module for the apis `/preprocess` and `/train`
+ The `dummy_API.py` under directory `/testdir` holds the dummy scipt for `/notify` api for implementing callback facility
+ The `statr.sh` scripts can be used to start all the server at one go


# Start the PREDICTION SERVER (/predict API):

+ `python predict_API.R` OR
  + use the `start.sh` file, run it as follows:
   + `./start.sh`
   + Remember to update the `start.sh` for port changing

## Run the client from terminal
  + following curl command can be used:
    + Syntax
	  + ``` curl http://localhost:<port number>/predict --data '[{"UID":"1","AGE":"15"},{"UID":"2","AGE":"12"},{"UID":"3","AGE":"55"},{"UID":"4","AGE":"37"}]' -H "Content-Type: application/json" ```
	+ `/predict` is the prediction API end point
	+ You may need to update the `port number` in the above curl command

# Start the Training SERVER (/preprocess and /train API):
  +  ` python train_API.py` OR
  + use the `start.sh` file and run `./start.sh`
+ As training and preprocessing can take several minutes, they should be called asynchronously using python package `threading` followed by a post call to the `callback API` for sending the status of preprocessing and training.

## Run the client from the terminal 
  + curl for preprocessing api `/preprocess`
    + ```curl http://localhost:<port number>/preprocess --data '{"callbackURL":"http://localhost:5020/notify"}' -H "Content-Type: application/json"```
  + curl for training api `/train`
    + ``` curl http://localhost:<port number>/train --data '{"callbackURL":"http://localhost:5020/notify"}' -H "Content-Type: application/json"```
  + The above `callbackURL` is a dummy api for testing. The dummy api script is in `/testdir` folder. Run the dummy callback API `python dummy_API.py`

