#!/usr/bin/python3
import requests, json
import sys
import netifaces
import os
from amscommon import read_config, write_config, put_device_info
config = read_config()

new_install = 0

# check to see if this is a new install.
try: 
   api_key = config['api_key']
except:
   new_install = 1
try: 
   device_id = config['device_id']
except:
   new_install = 1

# cam id or API key don't exist. 

# register device with AMS
eth0_mac = netifaces.ifaddresses('eth0')[netifaces.AF_LINK][0]['addr']
wlan0_mac = netifaces.ifaddresses('wlan0')[netifaces.AF_LINK][0]['addr']

try:
    eth0_ip = netifaces.ifaddresses('eth0')[netifaces.AF_INET][0]['addr']
except:
    eth0_ip = "0.0.0.0"
try:
    wlan0_ip= netifaces.ifaddresses('wlan0')[netifaces.AF_INET][0]['addr']
except:
    wlan0_ip = "0.0.0.0"

print ("ETH0 MAC: ", eth0_mac)
print ("WLAN MAC: ", wlan0_mac)
print ("ETH0 IP: ", eth0_ip)
print ("WLAN IP: ", wlan0_ip)

try:
   r = requests.get('http://www.amsmeteors.org/members/api/cam_api/mkdevice?format=json&LAN_MAC=' + eth0_mac + '&WLAN_MAC=' + wlan0_mac + '&lan_ip=' + eth0_ip + 'wlan_ip=' + wlan0_ip)
   fp = open("register.txt", "w")
   fp.write(r.text)
   fp.close()
except:
   print ("mkdevice failed.")

data = json.loads(r.text)
try:
   if data['errors']['Invalid_data'] == 'LAN_MAC WLAN_MAC combination must be unique.':
      print ("Device already created.")
   else:
      print ("Device created.")
except:
   print ("Device Created.")
  
#LOG IP OF DEVICE. 
msg = "lan_ip=" + eth0_ip + ":wlan_ip=" + wlan0_ip
r = requests.post('http://www.amsmeteors.org/members/api/cam_api/addLog', data={'LAN_MAC': eth0_mac, 'WLAN_MAC': wlan0_mac, 'msg': msg})

res = r.text

x, id = res.split("device_id: ")

hostname = "ams" + id.rstrip("\n")
print ("ID: ", hostname)
out = open("/home/pi/fireball_camera/host", "w") 
out.write(hostname)
out.close()
#os.system("sudo cp /home/pi/fireball_camera/host /etc/hostname")

#exit()

# GET THE DEVICE INFO

r = requests.get('http://www.amsmeteors.org/members/api/cam_api/get_device_info?format=json&LAN_MAC=' + eth0_mac + '&WLAN_MAC=' + wlan0_mac)
#print (r.text)
fp = open("device_info.txt", "w")
fp.write(r.text)
fp.close()

data = json.loads(r.text)
try: 
   for key in data['result'][1]:
      print (key)

   dev_data = data['result'][0]['cam'][0]
   operator_data = data['result'][1]['operator'][0]
   for key in operator_data:
      if type(operator_data[key]) is str:
         print (key, operator_data[key])
         config[key]=operator_data[key]

   for key in dev_data:
      if type(dev_data[key]) is str:
         print (key, dev_data[key])
         config[key]=dev_data[key]
   write_config(config)
   put_device_info(config)
except: 
   print ("Device is not claimed yet.")



