#!/usr/bin/python3
#this script sets up the cameras default params
# important backdoor URLS
# OSD - /videoosd.asp?
# Settings - /videolens.asp


import requests
from amscommon import read_config

config = read_config()

cam_ip = config['cam_ip']
#device_id = config['device_id']

print ("Setting up defaults for camera on IP address:", cam_ip)

print ("Set timezone and NTP server.")
url = "http://" + str(cam_ip) + "/cgi-bin/date_cgi?action=set&user=admin&pwd=admin&timezone=14&ntpHost=clock.isc.org"
print (url)
r = requests.get(url)
print (r.text)


print ("Set the OSD settings.")
url = "http://" + str(cam_ip) + "/cgi-bin/textoverlay_cgi?action=set&user=admin&pwd=admin&channel=0&Title=" + str("AMS") + "&DateValue=1&TimeValue=1&WeekValue=0&BitrateValue=0&Color=2&TitleValue=0"
print (url)
r = requests.get(url)
print (r.text)

url = "http://" + str(cam_ip) + "/webs/btnSettingEx?flag=2000&paramchannel=0&paramcmd=2005&paramctrl=0&paramstep=0&paramreserved=0"
print (url)
for x in range(0,140):
    r = requests.get(url)
    print (r.text)


url = "http://" + str(cam_ip) + "/webs/btnSettingEx?flag=2000&paramchannel=0&paramcmd=2006&paramctrl=0&paramstep=0&paramreserved=0"
print (url)
for x in range(0,138):
    r = requests.get(url)
    print (r.text)

#LSC CLOSE 
url = "http://" + str(cam_ip) + "/webs/btnSettingEx?flag=1000&paramchannel=0&paramcmd=1048&paramctrl=0&paramstep=0&paramreserved=0"
print (url)
r = requests.get(url)
print (r.text)

#CTB COLOR 
url = "http://" + str(cam_ip) + "/webs/btnSettingEx?flag=1000&paramchannel=0&paramcmd=1036&paramctrl=0&paramstep=0&paramreserved=0"
print (url)
r = requests.get(url)
print (r.text)

#WDR Closed
url = "http://" + str(cam_ip) + "/webs/btnSettingEx?flag=1000&paramchannel=0&paramcmd=1037&paramctrl=0&paramstep=0&paramreserved=0"
print (url)
r = requests.get(url)
print (r.text)

#3D-DNR Normal
url = "http://" + str(cam_ip) + "/webs/btnSettingEx?flag=1000&paramchannel=0&paramcmd=1049&paramctrl=3&paramstep=0&paramreserved=0"
print (url)
r = requests.get(url)
print (r.text)

url = "http://" + str(cam_ip) + "/webs/btnSettingEx?flag=1000&paramchannel=0&paramcmd=1050&paramctrl=3&paramstep=0&paramreserved=0"
print (url)
r = requests.get(url)
print (r.text)

# IR CONTROL TO TIME UTC 5pm to 7am open it up
url = "http://" + str(cam_ip) + "/webs/btnSettingEx?flag=1000&paramchannel=0&paramcmd=1063&paramctrl=1&paramstep=0&paramreserved=0"
print (url)
r = requests.get(url)
print (r.text)

url = "http://" + str(cam_ip) + "/webs/btnSettingEx?flag=1000&paramchannel=0&paramcmd=1081&paramctrl=1&paramstep=0&paramreserved=0"
print (url)
r = requests.get(url)
print (r.text)



url = "http://" + str(cam_ip) + "/webs/videoLensCfgEx?irtodayh=11&irtonighth=20"
print (url)
r = requests.get(url)
print (r.text)

# default shutter speed of 50

r = requests.get("http://" + config['cam_ip'] + "/webs/btnSettingEx?flag=1000&paramchannel=0&paramcmd=1058&paramctrl=50&paramstep=0&paramreserved=0&")


print ("Set the video encoding params.")
url = "http://" + str(cam_ip) + "/cgi-bin/videocoding_cgi?action=set&user=admin&pwd=admin&channel=0&EncType1=H.264&Resolution1=1280*720&BitflowType1=VBR&KeyInterval1=5&Bitrate1=512&FrameRate1=5&Profile1=Main Profile&PicLevel1=1"

print (url)
r = requests.get(url)
print (r.text)

url = "http://" + str(cam_ip) + "/cgi-bin/videocoding_cgi?action=set&user=admin&pwd=admin&channel=0&EncType2=H.264&Resolution2=640*480&KeyInterval2=25&FrameRate2=25&BitflowType2=VBR&NormalBitrate2=2048&PicLevel2=1&Profile2=Main Profile&quality2=1&ratectrl2=1"
print (url)
r = requests.get(url)
print (r.text)

