# This script tries to call the MARINE and PYTHIYA/MARINE API and compare 
#result for validation

import requests
import json
import urllib
import numpy as np
import gzip
import sys

def call_marine(pld):
	
	url_marine = 'http://scl000003187.sccloud.swissre.com:8040/predict'
	#payload_marine_dflt = '''{"input":[{"UID":"1","AGE":"asdf","NORM_GT":"asdf","AGG_TYPE":"CHEMICAL_TANKER","FLAG_GRADE":"M","MANAGER_INCIDENT_RATE":0.01},{"UID":"2","AGE":"asdf","NORM_GT":"1.1","AGG_TYPE":"MULTIPURPOSE","FLAG_GRADE":"H","MANAGER_INCIDENT_RATE":0.02},{"UID":"3","AGE":"15","NORM_GT":"0","AGG_TYPE":"CHEMICAL_TANKER","FLAG_GRADE":"M","MANAGER_INCIDENT_RATE":0.01},{"UID":"4","AGE":"-56","NORM_GT":"1.1","AGG_TYPE":"MULTIPURPOSE","FLAG_GRADE":"H","MANAGER_INCIDENT_RATE":0.02}]}'''
	
	payload_marine = pld
	#print payload_marine
	#print 
	#print payload_marine
	#print "\n"
	#payload_marine = pld
	#headers = {"Content-Type": "application/json"}
	response_marine = requests.post(url_marine,data = payload_marine)
	print "standalone marine api status code:"+ str(response_marine.status_code)
	print "******************"
	#print "headers:"+ str(response_marine.headers)
	#print "******************"
	#print "content:"+ str(response_marine.text)

	return response_marine.text


def call_pythia(pld):

	url_pythia = 'http://scl000003629.sccloud.swissre.com:3000/api/Projects/marine/solver/totalLoss/scoring'
	
	#inputdata = '[{"UID":"1","AGE":"15","NORM_GT":"0","AGG_TYPE":"CHEMICAL_TANKER","FLAG_GRADE":"M","MANAGER_INCIDENT_RATE":0.01},{"UID":"2","AGE":"asdf","NORM_GT":"1.1","AGG_TYPE":"MULTIPURPOSE","FLAG_GRADE":"H","MANAGER_INCIDENT_RATE":0.02},{"UID":"3","AGE":"15","NORM_GT":"0","AGG_TYPE":"CHEMICAL_TANKER","FLAG_GRADE":"M","MANAGER_INCIDENT_RATE":0.01},{"UID":"4","AGE":"-56","NORM_GT":"1.1","AGG_TYPE":"MULTIPURPOSE","FLAG_GRADE":"H","MANAGER_INCIDENT_RATE":0.02}]'
	#data = urllib.quote_plus(inputdata)	
	
	#payload_pythia = 'record='+str(data)
	payload_pythia = pld

	#headers = {"Content-Type": "application/json"}
	headers = {"Content-Type": "application/json","Accept": "application/json"}
	response_pythia = requests.post(url_pythia,data = payload_pythia, headers = headers)
	print "pythia_marine api status code:"+ str(response_pythia.status_code)
	print "******************"
	#print "headers:"+ str(response_pythia.headers)
	#print "******************"
	#print "content:"+ str(response_pythia.text)
	
	return response_pythia.text

def process_marine(filename):
	# read the json file as a string. NOT like a json in this scenario.
	with gzip.open(filename,'r') as fin:
		d = fin.readline()
	
	p='{"input":'+str(d)+'}'
	rm = json.loads(str(call_marine(p)))
	
	#print "+++++++++++++++++++++++++++++++++"
	#print type(rm)
	#print len(rm)
	#print rm

	n = len(rm)

	result_array = []
	for i in xrange(0,n):
		result_array.append(float(rm[i]['TLO_PROBA'][0]))
	
	return result_array


def process_pythia(filename):
	
	with gzip.open(filename,'r') as fin:
		d = fin.readline()
	
	#data = urllib.quote_plus(d)
	#pld = 'record='+str(data)

	data = d
	pld = str(data)

	#print pld
	#print "======="
	pm = json.loads(str(call_pythia(pld)))
	
	n = len(pm)
	#print pm
	result_array = []
	for i in xrange(0,n):
		result_array.append(float(pm[i]['TLO_PROBA']))

	return result_array

def main():

	n = int(sys.argv[1])
	filename = 'test_data_'+str(n)+'.json.gz'
	pmr = np.array(process_marine(filename))
	ppr = np.array(process_pythia(filename))
	
	#print "from Pythia"
	#print ppr
	#print
	#print "from marine"
	#print pmr
	#print
	print "Difference: %f" %(np.sum(pmr - ppr))

	print "done"

if __name__ == "__main__":
	main()
