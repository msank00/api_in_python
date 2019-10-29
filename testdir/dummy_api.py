import argparse
import json
import logging

import numpy as np
import pandas as pd
from flask import Flask, Response, jsonify, request

# UNCOMMENT THE FOLLOWING LINE FOR OPTIONAL ARGUMENT PARSER
# setting optional argument parser
parser = argparse.ArgumentParser(description="Get Hosting parameters")
parser.add_argument("--optHost", type=str, help="An optional Host Name")
parser.add_argument("--optPort", type=int, help="An optional port Number")
parser.add_argument("--logLevel", type=str, help="Logging level")
args = parser.parse_args()

# creating an instance of the Flask APP
app = Flask(__name__)


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


@app.route("/notify", methods=["POST"])
def notifyapiUtility():

    getClientInformation(request)
    try:
        # extrating data from the client request
        content = request.json  # get_json(silent=True)
        # content = json.loads(json.dumps(content))

        # print content
        # print type(content)

        print(content["task_type"])
        print(content["status_message"])
        print(content["unix_time"])

        # passing data to prediction module
        # output = predictionModule(contentdf)
        # outjson = output.to_json(orient='records')

        # creating the response to send back to the client
        # resp = Response(outjson,status=200,mimetype='application/json')
        # app.logger.info("----- REQUEST SERVED -----")

        output = {"Message": "Callback status received"}
        outjson = json.dumps(output)

        # creating the response to send back to the client
        resp = Response(outjson, status=200, mimetype="application/json")
        app.logger.info("----- REQUEST SERVED -----")

        return resp
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
    port = 5020

    logPath = "dummy_api_server.log"
    configLogging(logPath)

    app.logger.info("SERVER STARTED ON  %s:%s" % (ip, port))
    app.run(host=ip, port=port)
