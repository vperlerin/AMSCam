#!/usr/bin/python3
from pathlib import Path
import os
import requests
from collections import deque
import multiprocessing
from amscommon import read_config
import cv2
import iproc 
import datetime
import time
import json
import syslog
import sys

config = read_config()

if int(config['hd']) == 1:
    cap = cv2.VideoCapture("rtsp://" + config['cam_ip'] + "/av0_0&user=admin&password=admin&tcp")
    resize = .25
else:
    cap = cv2.VideoCapture("rtsp://" + config['cam_ip'] + "/av0_1&user=admin&password=admin&tcp")
    resize = .5 


count = 0
while cap.isOpened():
    ret,frame = cap.read()
    #debug on py
    if ret:
        #cv2.imshow('window-name',frame)
        cv2.imwrite("/var/www/html/out/latest.jpg", frame)
    break

api_key = config['api_key']
device_id  = config['device_id']
url = "http://www.amsmeteors.org/members/api/cam_api/upload_latest"
file = "/var/www/html/out/latest.jpg"
stat = os.stat(file)
#print (stat)
#datetime = stat.st_birthtime
dt = datetime.datetime.fromtimestamp(stat.st_ctime).strftime('%Y-%m-%d %H:%M:%S')
 
# usage: python upload.py type misc_info datetime filename 
# ex: python uploadLatest.py 2016-09-09%2020:03:02 some_info test.jpg
  
#datetime = sys.argv[1]
#misc_info = sys.argv[2]

# The File to send
_file = {'file_data': open(file, 'rb')}

# The Data to send with the file
_data= {'api_key': api_key, 'device_id': device_id, 'datetime': dt, 'format' : 'json'}
 
session = requests.Session()
del session.headers['User-Agent']
del session.headers['Accept-Encoding'] 

with requests.Session() as session:
    response = session.post(url, data= _data, files=_file)
 
print json.dumps(json.loads(response.text), ensure_ascii=False, encoding="utf-16")
response.raw.close() 

