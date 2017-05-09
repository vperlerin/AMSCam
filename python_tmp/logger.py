#!/usr/bin/python3

import requests
import sys
from amscommon import read_config

# usage: python logger.py type msg
# type = type of log message (reboot, system, capture, calibration) 
# msg = log message 

config = read_config()

msg = sys.argv[1]

r = requests.post('http://www.amsmeteors.org/members/api/cam_api/addLog', data={'device_id': config['device_id'], 'api_key': config['api_key'], 'msg': msg})
print (r.text)
