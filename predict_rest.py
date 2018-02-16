from flask import Flask, request
import os
import csv
import json
import copy
import re as re
import jsonpickle
import jsonpickle.ext.numpy as jsonpickleNumpy
import numpy as np
jsonpickleNumpy.register_handlers()
import pandas as pd
import StringIO
import sys
import os.path
if sys.version_info[0] < 3:
    from StringIO import StringIO
else:
    from io import StringIO
import logging
import argparse

parser = argparse.ArgumentParser(description='Get Hosting parameters')
parser.add_argument('--optHost', type=str,  help='An optional Host Name')
parser.add_argument('--optPort', type=int,  help='An optional port Number')
parser.add_argument('--logLevel', type=str,  help='Logging level')
args = parser.parse_args()
app = Flask(__name__)

requiredJsonFlds = ["PassengerId", "Pclass", "Name", "Sex", "Age", "SibSp", "Parch", "Ticket", "Fare", "Cabin", "Embarked"]
nonEmptyFields = ["PassengerId","Name","Sex","Pclass","Age"]
numericFields = ["Age","Fare","Pclass","SibSp","Parch"]
nonNegetiveFields = ["Age","Fare","Pclass","SibSp","Parch"]
modelJonPath = "datacontainer/training/titanicmodel.json"
trainDatasetpath = "datacontainer/training/train.csv"
logPath = "titanicRestService.log"
responceJson = "{}" # change it to non global

from enum import Enum
class ResponseCode(Enum):
    UnsupportedMediaType = 415
    OK = 200
    BadRequest = 400

@app.route('/')
def apiRoot():
    return 'Titanic Prediction Model'

@app.route('/validate', methods = ['POST'])
def apiValidate():
    try:
        responceJsonObj = json.loads(responceJson)
        paramStr = json.dumps(request.json)
        if request.headers['Content-Type'] == 'application/json':
            responceJsonObj, jsonDoc, warJsonArray, resCode = validate(paramStr, responceJsonObj)
            count = 0
            if(len(responceJsonObj)==0):
                responceJsonObj = []
            for rec in jsonDoc:
                if(warJsonArray[count]!=None):
                    rec["STATUS"] = warJsonArray[count]
                else:
                    rec["STATUS"] = "OK"
                count += 1
                responceJsonObj.append(rec)
            return json.dumps(responceJsonObj), resCode.value
        else:
            app.logger.error('Unsupported Media Type')
            responceJsonObj["STATUS"] = {"ERROR": "Unsupported Media Type"}
            return json.dumps(responceJsonObj), ResponseCode.UnsupportedMediaType.value
    except Exception as e:
        app.logger.exception("message")
        raise Exception(e)

@app.route('/predict', methods = ['POST'])
def apiPredict():
    try:
        responceJsonObj = json.loads(responceJson)
        paramStr = json.dumps(request.json)
        app.logger.info('Input Json: %s'%paramStr)
        if request.headers['Content-Type'] == 'application/json':
            responceJsonObj, jsonArray, warJsonArray, resCode = validate(paramStr, responceJsonObj)
            if resCode !=ResponseCode.OK and len(jsonArray)==0:
                return json.dumps(responceJsonObj), resCode.value
            responceJsonObj = pridict(jsonArray, responceJsonObj, warJsonArray)
            return json.dumps(responceJsonObj)
        else:
            app.logger.error('Unsupported Media Type')
            responceJsonObj["STATUS"] = {"ERROR": "Unsupported Media Type"}
            return json.dumps(responceJsonObj), ResponseCode.UnsupportedMediaType.value
    except Exception as e:
        app.logger.exception("message")
        raise Exception(e)

def validate(jsonDoc,responceJsonObj):
    rtnJsonArray = []
    errJsonArray = []
    warJsonArray= []
    retn, validJson = isJson(jsonDoc)
    if not retn:
        responceJsonObj["STATUS"] = {"ERROR": "Invalid Json"}
        app.logger.error('Invalid Json')
        return responceJsonObj, rtnJsonArray, warJsonArray, ResponseCode.BadRequest
    if not isinstance(validJson, list):
        responceJsonObj["STATUS"] = {"ERROR": "Json array expected"}
        app.logger.error('Json array expected')
        return responceJsonObj, rtnJsonArray, warJsonArray, ResponseCode.BadRequest
    elif len(validJson)==0:
        responceJsonObj["STATUS"] = {"ERROR": "No Json data to process"}
        app.logger.error('No Json data to process')
        return responceJsonObj, rtnJsonArray, warJsonArray, ResponseCode.BadRequest

    for item in validJson:
        reqFieldErr = {}
        warFields = {}
        for att in requiredJsonFlds:
            try:
                if not item[att] and att in nonEmptyFields:
                    reqFieldErr[att] = "Field must not be empty"
                if item[att] and att in numericFields:
                    try:
                        float(item[att])
                    except ValueError as e:
                        reqFieldErr[att] = "Field must be Numeric"
                if item[att] and att in nonNegetiveFields:
                    try:
                        if float(item[att])<0:
                            warFields[att] = "The value is negative"
                    except ValueError as e:
                        reqFieldErr[att] = "Field must be Numeric"
            except KeyError as e:
                reqFieldErr[att] = "Field is missing"
        if len(reqFieldErr)>0:
            itemCopy = copy.deepcopy(item)
            errfieldList = []
            for  fld in reqFieldErr:
                errfieldList.append({"FIELD":fld,"ERROR":reqFieldErr[fld]})
            if len(warFields)>0:
                for fld in warFields:
                    errfieldList.append({"FIELD":fld, "WARNING": warFields[fld]})
                    app.logger.warning("WARNING: FIELD %s: %s "%(fld, warFields[fld]))
            itemCopy["STATUS"] = errfieldList
            errJsonArray.append(itemCopy)
        if len(warFields)>0 and len(reqFieldErr)==0:
            warFieldList = []
            for fld in warFields:
                warFieldList.append({"FIELD":fld, "WARNING": warFields[fld]})
                app.logger.warning("WARNING: FIELD %s: %s "%(fld, warFields[fld]))
            warJsonArray.append(warFieldList)
        if len(warFields)==0 and len(reqFieldErr)==0:
            warJsonArray.append(None)
        if len(reqFieldErr)==0:
            rtnJsonArray.append(item)
    if len(errJsonArray)>0:
        responceJsonObj = errJsonArray
        return responceJsonObj, rtnJsonArray, warJsonArray, ResponseCode.BadRequest
    else:
        return responceJsonObj, rtnJsonArray, warJsonArray, ResponseCode.OK

def pridict(jsonArray, responceJsonObj, warJsonArray):
    jsonDoc =  json.loads(json.dumps(jsonArray))
    csvFileObj = jsonToCSV(jsonDoc)
    pridictDf = pd.read_csv(StringIO(csvFileObj), header = 0, dtype={'Age': np.float64})

    iterDfForNumaricNan(pridictDf,'SibSp')
    iterDfForNumaricNan(pridictDf,'Parch')
    pridictDf['FamilySize'] = pridictDf['SibSp'] + pridictDf['Parch'] + 1
    pridictDf['Embarked'] = pridictDf['Embarked'].fillna('S')
    iterDfForNumaricNan(pridictDf,'Fare')
    pridictDf['Fare'] = pridictDf['Fare'].fillna(pridictDf['Fare'].median())

    iterDfForNumaricNan(pridictDf,'Age')
    #categorizing Fare in to different Fare Bucket based upon qualtile
    #pridictDf['CategoricalFare'] = pd.qcut(pridictDf['Fare'], 1)
    '''age_avg 	   = pridictDf['Age'].mean()
    age_std 	   = pridictDf['Age'].std()
    age_null_count = pridictDf['Age'].isnull().sum()
    age_null_random_list = np.random.randint(age_avg - age_std, age_avg + age_std, size=age_null_count)
    pridictDf['Age'][np.isnan(pridictDf['Age'])] = age_null_random_list'''
    pridictDf['Age'] = pridictDf['Age'].astype(int)
    #pridictDf['CategoricalAge'] = pd.cut(pridictDf['Age'], 5)

    pridictDf['Title'] = pridictDf['Name'].apply(getTitle)
    pridictDf['Title'] = pridictDf['Title'].replace(['Lady', 'Countess','Capt', 'Col', \
                                                     'Don', 'Dr', 'Major', 'Rev', 'Sir', 'Jonkheer', 'Dona'], 'Rare')
    pridictDf['Title'] = pridictDf['Title'].replace('Mlle', 'Miss')
    pridictDf['Title'] = pridictDf['Title'].replace('Ms', 'Miss')
    pridictDf['Title'] = pridictDf['Title'].replace('Mme', 'Mrs')
    # Mapping Sex
    pridictDf['Sex'] = pridictDf['Sex'].map( {'female': 0, 'male': 1} ) #.astype(int)
    # Mapping titles
    titleMapping = {"Mr": 1, "Miss": 2, "Mrs": 3, "Master": 4, "Rare": 5}
    pridictDf['Title'] = pridictDf['Title'].map(titleMapping)
    pridictDf['Title'] = pridictDf['Title'].fillna(0)
    # Mapping Embarked
    pridictDf['Embarked'] = pridictDf['Embarked'].map( {'S': 0, 'C': 1, 'Q': 2} ) #.astype(int)
    #  Mapping Fare
    pridictDf.loc[ pridictDf['Fare'] <= 7.91, 'Fare'] 						        = 0
    pridictDf.loc[(pridictDf['Fare'] > 7.91) & (pridictDf['Fare'] <= 14.454), 'Fare'] = 1
    pridictDf.loc[(pridictDf['Fare'] > 14.454) & (pridictDf['Fare'] <= 31), 'Fare']   = 2
    pridictDf.loc[ pridictDf['Fare'] > 31, 'Fare'] 							        = 3
    pridictDf['Fare'] = pridictDf['Fare'].astype(int)
    # Mapping Age
    pridictDf.loc[ pridictDf['Age'] <= 16, 'Age'] 					       = 0
    pridictDf.loc[(pridictDf['Age'] > 16) & (pridictDf['Age'] <= 32), 'Age'] = 1
    pridictDf.loc[(pridictDf['Age'] > 32) & (pridictDf['Age'] <= 48), 'Age'] = 2
    pridictDf.loc[(pridictDf['Age'] > 48) & (pridictDf['Age'] <= 64), 'Age'] = 3
    pridictDf.loc[ pridictDf['Age'] > 64, 'Age']                           = 4
    # Feature Selection
    dropElements = ['PassengerId', 'Name', 'Ticket', 'Cabin', 'SibSp', \
                     'Parch', 'FamilySize']
    pridictDf = pridictDf.drop(dropElements, axis = 1)
    #pridictDf = pridictDf.drop(['CategoricalAge', 'CategoricalFare'], axis = 1)
    #pridictDf = pridictDf.drop(['CategoricalAge'], axis = 1)
    pridictDf = pridictDf.values
    filehandler = open(modelJonPath, 'r')

    jsonCandidateClassifier = jsonpickle.decode(filehandler.read())
    result = jsonCandidateClassifier.predict(pridictDf)

    if(len(responceJsonObj)==0):
        responceJsonObj = []
    count = 0
    for rec in jsonDoc:
        rec["Prediction"] = str(result[count])
        if(warJsonArray[count]!=None):
            rec["STATUS"] = warJsonArray[count]
        count += 1
        responceJsonObj.append(rec)
    return responceJsonObj

def iterDfForNumaricNan(df,col):
    if(df[col].dtype == np.float64 or df[col].dtype == np.int64):
        for index, row in df.iterrows():
            if np.isnan(row[col]):
                meanValue = getFromTrainningData(col)
                app.logger.info("getting mean value from training data set for the Nan field %s as '%s'"%col,meanValue)
                df.set_value(index,col,meanValue)

def getFromTrainningData(col):
    return train[col].mean()

def getTitle(name):
    titleSearch = re.search(' ([A-Za-z]+)\.', name)
    # If the title exists, extract and return it.
    if titleSearch:
        return titleSearch.group(1)
    return ""

def isJson(doc):
    jsonObject = None
    try:
        jsonObject = json.loads(doc)
    except ValueError as e:
        return False, jsonObject
    return True, jsonObject

def jsonToCSV(jsonObject):
    count = 0
    si = StringIO()
    cw = csv.writer(si)
    for rec in jsonObject:
        if count == 0:
            header = rec.keys()
            cw.writerow(header)
            count += 1
        cw.writerow(rec.values())
    return si.getvalue().strip('\r\n')

def configLogging():
    if args.logLevel and len(args.logLevel)>0:
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
    fileHandler.setFormatter(Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]'
    ))
    fileHandler.setLevel(logLvl)
    app.logger.addHandler(fileHandler)
    app.logger.setLevel(logLvl)

@app.errorhandler(404)
def pageNotFound(error):
    responceJsonObj = json.loads(responceJson)
    responceJsonObj["STATUS"] = {"ERROR": "This page does not exist"}
    return json.dumps(responceJsonObj), 404

@app.errorhandler(500)
@app.errorhandler(Exception)
def handledException(e):
    responceJsonObj = json.loads(responceJson)
    responceJsonObj["STATUS"] = {"ERROR": "Exception: %s"%(e)}
    app.logger.error("Exception: %s"%(e))
    return json.dumps(responceJsonObj), 500

if __name__ == '__main__':

    ip = "127.0.0.1"
    port = "5000"
    configLogging()

    if not os.path.isfile(modelJonPath):
        app.logger.exception("No such file '%s'"%modelJonPath)
        sys.exit(1)
    if not os.path.isfile(trainDatasetpath):
        app.logger.exception("No such file '%s'"%trainDatasetpath)
        sys.exit(1)
    train = pd.read_csv(trainDatasetpath, header = 0, dtype={'Age': np.float64})
    app.logger.info("started running on  %s:%s"%(ip,port))
    if args.optHost and len(args.optHost)>0:
        ip = args.optHost
    if args.optPort and len(args.optPort)>0:
        port = args.optPort

    app.run(host=ip, port=port)
