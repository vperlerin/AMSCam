#!/usr/bin/python3
import requests
import mimetypes
import sys
from pathlib import Path
from amscommon import read_config, write_config

# UPLOAD CALIBRATION FILES AND STATUS

config = read_config()

try:
   el = sys.argv[1].split("/")
   caldate= el[-1]
   file = "/var/www/html/out/cal/" + caldate 
except:
   print ("Usage: ./upload_calibration.py file.jpg")
   exit()
file_exists = Path(file)
if (file_exists.is_file()):
   print("File found.")
else:
   print("File not found:", file)
   exit()
y = caldate[0:4]
m = caldate[4:6]
d = caldate[6:8]
h = caldate[8:10]
mm = caldate[10:12]
s = caldate[12:14]
caldate = y + "-" + m + "-" + d + " " + h + ":" + mm + ":" + s

api_key = config['api_key'] 
device_id  = config['device_id']
url = "http://www.amsmeteors.org/members/api/cam_api/log_calibration_files"

# usage: python upload.py type misc_info datetime filename 
# ex: python log_calibration_files.py  
star_file   = file;
wcs_file    = file.replace(".jpg", ".wcs")
const_file  = file.replace(".jpg", "-grid.png")
cal_file = y + m + d + h + mm + s 

# Check that WCS file exists else cal failed.
file_exists = Path(wcs_file)
if (file_exists.is_file()):
   print("Calibration was successful.")
   config['best_caldate'] = cal_file
   # The Files to send
   _file = {'stars': open(star_file, 'rb'), 'wcs': open(wcs_file, 'rb'), 'constellation': open(const_file, 'rb')}
   _data= {
    'api_key': api_key, 
    'device_id': device_id, 
    'format': 'json',
    'datetime': caldate,
    'center_ra_dec' : config['center_ra_dec'],
    'center_az_el' : config['center_az_el'],
    'pixel_scale' : config['pixel_scale'],
    'ulc_ra_dec' : config['ulc_ra_dec'],
    'urc_ra_dec' : config['urc_ra_dec'],
    'llc_ra_dec' : config['llc_ra_dec'],
    'lrc_ra_dec' : config['lrc_ra_dec'],
    'ulc_az_el' : config['ulc_az_el'],
    'urc_az_el' : config['urc_az_el'],
    'llc_az_el' : config['llc_az_el'],
    'lrc_az_el' : config['lrc_az_el'],
   }

else:
   print("This calibration failed.", wcs_file)
   status = "failed" 
   _file = {'stars': open(star_file, 'rb')}
   # The Data to send with the file
   _data= {
      'api_key': api_key, 
      'device_id': device_id, 
      'format': 'json',
      'datetime': caldate,
      'status' : status
   }

write_config(config)
session = requests.Session()
del session.headers['User-Agent']
del session.headers['Accept-Encoding'] 

with requests.Session() as session:
    response = session.post(url, data= _data, files=_file)
 
print (response.text)
response.raw.close() 
