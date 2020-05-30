import argparse
import calendar
import json
import logging
import threading as th
import time
from datetime import datetime

import numpy as np
import pandas as pd
import requests as req
from flask import Flask, Response, jsonify, request

# UNCOMMENT THE FOLLOWING LINE FOR OPTIONAL ARGUMENT PARSER
# setting optional argument parser
parser = argparse.ArgumentParser(description="Get Hosting parameters")
parser.add_argument("--optHost", type=str, help="An optional Host Name")
parser.add_argument("--optPort", type=str, help="An optional port Number")
parser.add_argument("--logLevel", type=str, help="Logging level")
args = parser.parse_args()

# creating an instance of the Flask APP
app = Flask(__name__)


def postStatus(a_callbackURL, a_status_message, a_task_type, a_unix_time):

    callbackAddress = a_callbackURL  #'http://localhost:5020/notify'
    task_type = a_task_type  # "preprocessing"
    status_message = a_status_message  # "OK"
    unix_time = a_unix_time  # 1234

    payload_notify = {}
    payload_notify["task_type"] = task_type
    payload_notify["status_message"] = status_message
    payload_notify["unix_time"] = unix_time

    # headers = {"Content-Type": "application/json"}
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    response = req.post(
        callbackAddress, data=json.dumps(payload_notify), headers=headers
    )
    callbackAPIstatus = "callback api status code:" + str(response.status_code)
    print(callbackAPIstatus)
    app.logger.info(callbackAPIstatus)
    # print "******************"
    # print "callback response headers:"+ str(response.headers)
    # print "******************"
    # print "callback response content:"+ str(response.text)
    # print response.text
    return


def getClientInformation(request):
    # logging client information
    app.logger.info("+++++ REQUEST RECEIVED +++++")
    req_method = request.environ["REQUEST_METHOD"]
    req_api = request.environ["PATH_INFO"]
    req_http_user_agent = request.environ["HTTP_USER_AGENT"]
    req_remote_address = request.environ["REMOTE_ADDR"]

    app.logger.info("REQUEST METHOD: %s" % (req_method))
    app.logger.info("REQUEST API: %s" % (req_api))
    app.logger.info("HTTP USER AGENT: %s" % (req_http_user_agent))
    app.logger.info("CLIENT ADDRESS: %s" % req_remote_address)
    return


@app.route("/preprocess", methods=["POST"])
def preprocessUtility():

    getClientInformation(request)
    try:
        # extrating data from the client request
        content = request.json  # get_json(silent=True)
        # content = json.dumps(content)
        callbackURL = content["callbackURL"]
        # print type(callbackURL)
        # print callbackURL

        # calling Preprocessing Module as a child thread (to implement asynchronous call)
        # with a callback api argument
        th.Thread(
            target=preprocessingModule, kwargs={"callbackURL": callbackURL}
        ).start()

        # parent process immediately sends a status back to the client
        # while the child process is running independently
        output = {"Preprocessing": "STARTED"}
        outjson = json.dumps(output)

        # creating the response to send back to the client
        resp = Response(outjson, status=200, mimetype="application/json")
        app.logger.info("----- REQUEST SERVED -----")

        return resp
    except Exception as e:
        app.logger.exception("message")
        raise Exception(e)


@app.route("/train", methods=["POST"])
def trainingUtility():

    getClientInformation(request)
    try:
        # extrating data from the client request
        content = request.json  # get_json(silent=True)
        # content = json.dumps(content)
        callbackURL = content["callbackURL"]
        # print type(callbackURL)
        # print callbackURL

        # calling Preprocessing Module as a child thread (to implement asynchronous call)
        # with a callback api argument
        th.Thread(
            target=trainingModule, kwargs={"callbackURL": callbackURL}
        ).start()

        # parent process immediately sends a status back to the client
        # while the child process is running independently
        output = {"Training": "STARTED"}
        outjson = json.dumps(output)

        # creating the response to send back to the client
        resp = Response(outjson, status=200, mimetype="application/json")
        app.logger.info("----- REQUEST SERVED -----")

        return resp
    except Exception as e:
        app.logger.exception("message")
        raise Exception(e)


# ==========original preprocessing module========
# .. here we have added a dumy for loop with sleep
# .. to simulate the time consuming algorithm and then
# .. we are making a callback to the given api
def preprocessingModule(callbackURL):

    try:
        # ====================================================
        # all the preprocessing algorithm function calls goes here
        # ====================================================

        print("Inside Preprocessing Task...\nIt may take some time...")
        for i in range(1, 10):
            print(i)
            time.sleep(1)

        app.logger.info("Preprocessing Successful")
        app.logger.info("POST status to callback API")

        task_type = "preprocess"
        status_message = "OK"
        unix_time = getUnixTime()

        print(task_type)
        print(status_message)
        print(unix_time)
        print(callbackURL)

        # posting status to callback api
        postStatus(callbackURL, status_message, task_type, unix_time)

        return

    except Exception as e:
        app.logger.exception("message")
        raise Exception(e)


# ==========original training module========
# .. here we have added a dumy for loop with sleep
# .. to simulate the time consuming algorithm and then
# .. we are making a callback to the given api
def trainingModule(callbackURL):

    try:
        # ====================================================
        # all the training algorithm function calls goes here
        # ====================================================

        print("Inside Training Module...\nIt may take some time...")
        for i in range(1, 15):
            print(i)
            time.sleep(1)

        app.logger.info("Training Successful")
        app.logger.info("POST status to callback API")

        task_type = "training"
        status_message = "OK"
        unix_time = getUnixTime()

        print(task_type)
        print(status_message)
        print(unix_time)
        print(callbackURL)

        # posting status to callback api
        postStatus(callbackURL, status_message, task_type, unix_time)

        return

    except Exception as e:
        app.logger.exception("message")
        raise Exception(e)


def getUnixTime():
    d = datetime.utcnow()
    unixtime = calendar.timegm(d.utctimetuple())
    return unixtime


def trayingModule(inputData):

    try:
        # ====================================================
        # all the preprocessing algorithm function calls goes here
        # ====================================================
        print(inputData)
        print("Inside Traying Module...\nIt may take some time...")
        time.sleep(5)
        print("Traying Successful")

    except Exception as e:
        app.logger.exception("message")
        raise Exception(e)


def configLogging(logPath):
    if args.logLevel and len(args.logLevel) > 0:
        if args.logLevel.upper() == "INFO":
            logLvl = logging.INFO
        elif args.logLevel.upper() == "DEBUG":
            logLvl = logging.DEBUG
        elif args.logLevel.upper() == "WARNING":
            logLvl = logging.WARNING
        elif args.logLevel.upper() == "ERROR":
            logLvl = logging.ERROR
        else:
            logLvl = logging.INFO
    else:
        logLvl = logging.INFO

    from logging import Formatter

    fileHandler = logging.FileHandler(logPath)
    fileHandler.setFormatter(
        Formatter(
            "%(asctime)s %(levelname)s: %(message)s "
            "[in %(pathname)s:%(lineno)d]"
        )
    )
    fileHandler.setLevel(logLvl)
    app.logger.addHandler(fileHandler)
    app.logger.setLevel(logLvl)


if __name__ == "__main__":

    ip = "127.0.0.1"
    port = "5001"

    logPath = "log/training_API_server.log"
    configLogging(logPath)

    if args.optHost and len(args.optHost) > 0:
        ip = args.optHost
    if args.optPort and len(args.optPort) > 0:
        port = args.optPort

    app.logger.info("SERVER STARTED ON  %s:%s" % (ip, port))
    app.run(host=ip, port=port)
