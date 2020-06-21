#!/usr/bin/env bash


# checking the port 5040, 5041 and if any processes are running
# it will kill them before starting the server	
# prediction API is running in 5040, to kill the training API, uncomment the 
# lines for the respective port
kill -9 $(lsof -i:5000 -t) 2> /dev/null
kill -9 $(lsof -i:5001 -t) 2> /dev/null
kill -9 $(lsof -i:5020 -t) 2> /dev/null


# for running the training API, uncomment the line
python predict_API.py &
python train_API.py &
python ../testdir/notify_api.py
