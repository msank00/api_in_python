#!/usr/bin/env bash


# checking the port 5040, 5041 and if any processes are running
# it will kill them before starting the server	
# prediction API is running in 5040, to kill the training API, uncomment the 
# lines for the respective port
kill -9 $(lsof -i:5040 -t) 2> /dev/null
kill -9 $(lsof -i:5041 -t) 2> /dev/null

# for running the training API, uncomment the line
Rscript run_prediction_API.R 5040&
Rscript run_training_API.R 5041 &
