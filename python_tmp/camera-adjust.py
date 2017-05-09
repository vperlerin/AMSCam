#!/usr/bin/python3 
import cv2
import subprocess 
import time
from collections import defaultdict
from amscommon import read_config, read_sun
import requests
from urllib.request import urlretrieve
import re



def get_cam_brightness(config):
#   urlretrieve("http://" + config['cam_ip'] + "/cgi-bin/images_cgi?channel=0&user=admin&pwd=admin", 'cam.jpg')
   cap = cv2.VideoCapture("rtsp://" + config['cam_ip'] + "/av0_0&user=admin&password=admin&tcp")
   _ , frame = cap.read()
   cv2.imwrite("/home/pi/fireball_camera/cam.jpg", frame)


   proc = subprocess.Popen( ["identify", "-verbose", "/home/pi/fireball_camera/cam.jpg"], stdout=subprocess.PIPE, shell=False)
   #proc = subprocess.Popen( ["identify", "-verbose", "/var/www/html/out/latest.jpg"], stdout=subprocess.PIPE, shell=False)
   (out, err) = proc.communicate()
   outstr = out.decode("utf-8")
   means = [0,0,0,0] 
   c = 0
   for line in outstr.splitlines():
      if "mean" in line:
         trash = re.findall(r"[\w']+", line)
         means[c] = trash[1]
         c = c + 1
        
   return(means)

def get_settings(config):
   url = "http://" + str(config['cam_ip']) + "/cgi-bin/videoparameter_cgi?action=get&user=admin&pwd=admin&action=get&channel=0"
   settings = defaultdict()
   r = requests.get(url)
   resp = r.text
   for line in resp.splitlines():
      (set, val) = line.split("=")
      settings[set] = val  
   return(settings)

def set_setting(config, setting, value):
   url = "http://" + str(config['cam_ip']) + "/cgi-bin/videoparameter_cgi?action=set&user=admin&pwd=admin&action=get&channel=0&" + setting + "=" + str(value)
   r = requests.get(url)
   return(r.text)

def adjust_brightness(config,settings,blow,bhigh,brightness_min, brightness_max):
   log = open("/var/www/html/out/log.txt", "a");
   means = get_cam_brightness(config)
   print ("BLOW/HIGH:", blow, bhigh)
   if int(means[3]) == 0:
      print ("Image totally black! error.")
      exit()

   if int(means[3]) > int(bhigh):
      print ("Image is too bright (" + str(means[3]) + ") at Brightness=" + settings['Brightness'])
      log.write("Image is too bright (" + str(means[3]) + ") at Brightness=" + settings['Brightness'])
      new_b = int(settings['Brightness']) - 5
      if new_b > brightness_min and new_b < brightness_max:
         resp = set_setting(config, "Brightness", new_b)
         return(0)
      else:
         print("Brightness out of range reseting..")
         resp = set_setting(config, "Brightness", brightness_max)
         exit()
         return(0)
   elif int(means[3]) < int(blow): 
      print ("Image is too dark(" + str(means[3]) + ") at Brightness=" + settings['Brightness'])
      log.write("Image is too dark(" + str(means[3]) + ") at Brightness=" + settings['Brightness'])
      new_b = int(settings['Brightness']) + 5 
      if new_b > int(brightness_min) and new_b < int(brightness_max):
         resp = set_setting(config, "Brightness", new_b)
         return(0)
      else:
         print("Brightness out of range reseting..")
         resp = set_setting(config, "Brightness", brightness_max)
         exit()
         return(0)
   else:
      log.write("Image is just right at overall mean brightness: " + str(means[3]))
      print ("Image is just right at overall mean brightness: " + str(means[3]))
      return(1)

config = read_config() 
sun_info = read_sun()


cam_settings = get_settings(config)

#set_setting(config, "Brightness", "1")
loop = 0
c = 0
while (c < 10):
   print("keep trying")
   cam_settings = get_settings(config)
   loop = adjust_brightness(config, cam_settings, blow,bhigh,brightness_min,brightness_max)
   time.sleep(2)
   c = c + 1
