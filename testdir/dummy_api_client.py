# This script tries to call the MARINE and PYTHIYA/MARINE API and compare 
#result for validation

import requests
import json

def postStatus():

	callbackAddress = 'http://localhost:5020/notify'
	task_type = "preprocessing"
        status_message = "OK"
        unix_time = 1234

        payload_notify = {}
        payload_notify['task_type'] = task_type
        payload_notify['status_message']=status_message
        payload_notify['unix_time']=unix_time



	#headers = {"Content-Type": "application/json"}
	headers = {"Content-Type": "application/json","Accept": "application/json"}
	response_pythia = requests.post(callbackAddress,data = json.dumps(payload_notify), headers = headers)
	print "pythia_marine api status code:"+ str(response_pythia.status_code)
	print "******************"
	print "headers:"+ str(response_pythia.headers)
	print "******************"
	print "content:"+ str(response_pythia.text)
	print response_pythia.text
        return


def main():
    postStatus()
    print "posting done"

if __name__ == "__main__":
	main()
