#!/usr/bin/python3

import time
from collections import defaultdict
from amscommon import read_config, read_sun
import os
import requests
from urllib.request import urlretrieve

def set_setting(config, setting, value):
   url = "http://" + str(config['cam_ip']) + "/cgi-bin/videoparameter_cgi?action=set&user=admin&pwd=admin&action=get&channel=0&" + setting + "=" + str(value)
   r = requests.get(url)
   return(r.text)

def get_settings(config):
   url = "http://" + str(config['cam_ip']) + "/cgi-bin/videoparameter_cgi?action=get&user=admin&pwd=admin&action=get&channel=0"
   settings = defaultdict()
   r = requests.get(url)
   resp = r.text
   for line in resp.splitlines():
      (set, val) = line.split("=")
      settings[set] = val
   return(settings)

def set_special(config, field, value):
   url = "http://" + str(config['cam_ip']) + "/webs/btnSettingEx?flag=1000&paramchannel=0&paramcmd=" + str(field) + "&paramctrl=" + str(value) + "&paramstep=0&paramreserved=0"
   print (url)
   r = requests.get(url)
   print (r.text)

def WDR(config, on):
   #WDR ON/OFF 
   url = "http://" + str(config['cam_ip']) + "/webs/btnSettingEx?flag=1000&paramchannel=0&paramcmd=1037&paramctrl=" + str(on) + "&paramstep=0&paramreserved=0"
   print (url)
   r = requests.get(url)
   print (r.text)

def nighttime_settings(config):
   print ("Nighttime settings...")
   fp = open("/home/pi/fireball_camera/calnow", "w")
   WDR(config, 0)
   ### BLC 
   set_special(config, "1017", "150")
   set_setting(config, "Brightness", 65)
   set_setting(config, "Contrast", "65")
   set_setting(config, "Gamma", "30")
   set_setting(config, "InfraredLamp", "high")
   set_setting(config, "TRCutLevel", "high")
   time.sleep(5)
   os.system("rm /home/pi/fireball_camera/calnow")

def daytime_settings(config):
   fp = open("/home/pi/fireball_camera/calnow", "w")
   ### 
   WDR(config, 1)
   ### IR mode
   set_special(config, "1064", "2")
   ### BLC 
   set_special(config, "1017", "75")

   set_setting(config, "Brightness", "135")
   set_setting(config, "Gamma", "50")
   set_setting(config, "Contrast", "128")
   set_setting(config, "InfraredLamp", "low")
   set_setting(config, "TRCutLevel", "low")
   os.system("rm /home/pi/fireball_camera/calnow")
   time.sleep(5)

config = read_config()

settings = get_settings(config)

sun = read_sun()
print (sun['status'])
if sun['status'] == 'day':
   if settings['Brightness'] != "135":
      daytime_settings(config)
else:
   if settings['Brightness'] != "65":
      nighttime_settings(config)
