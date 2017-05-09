#!/usr/bin/python3 
import ephem
import time

def deg_to_dms(deg):
    d = int(deg)
    md = abs(deg - d) * 60
    m = int(md)
    sd = (md - m) * 60
    return [d, m, sd]

def read_config():
    config = {}
    file = open("config.txt", "r")
    for line in file:
      line = line.strip('\n')
      data = line.rsplit("=",2)
      config[data[0]] = data[1]
      #print key, value
    try:
       config['az_left'] = int(config['cam_heading']) - (int(config['cam_fov_x'])/2)
       config['az_right'] = int(config['cam_heading']) + (int(config['cam_fov_x'])/2)
       if (config['az_right'] > 360):
          config['az_right'] = config['az_right'] - 360
       if (config['az_left'] > 360):
          config['az_left'] = config['az_left'] - 360
       if (config['az_left'] < 0):
          config['az_left'] = config['az_left'] + 360
       config['el_bottom'] = int(config['cam_alt']) - (int(config['cam_fov_y'])/2)
       config['el_top'] = int(config['cam_alt']) + (int(config['cam_fov_y'])/2)
    except:
       print ("camera not yet calibrated.")
       config['az_left'] = 0
       config['az_right'] = 0
    return(config)


config = read_config()


obs = ephem.Observer()
obs.pressure = 0
obs.horizon = '-0:34'
#print (deg_to_dms(float(config['device_lat'])))
#print (deg_to_dms(float(config['device_lng'])))
obs.lat = config['device_lat']
obs.lon = config['device_lng']
cur_date = time.strftime("%Y/%m/%d %H:%M") 
print ("CUR DATE: ", cur_date)
obs.date = cur_date

sun = ephem.Sun()
sun.compute(obs)

#print (obs.lat, obs.lon, obs.date)

(sun_alt, x,y) = str(sun.alt).split(":")
print ("Sun Alt: %s" % (sun_alt))

saz = str(sun.az)
(sun_az, x,y) = saz.split(":")
print ("SUN AZ IS : %s" % sun_az)
print ("CAM FOV IS : %s to %s " % (config['az_left'], config['az_right']))

if (int(sun_az) >= config['az_left'] and int(sun_az) <= config['az_right']):
   print ("Uh Oh... Sun is in the cam's field of view.")
   fov=1
else:
   print ("Sun is not in the cam's field of view")
   fov=0

#print (obs.previous_rising(ephem.Sun()))
#print (obs.next_setting(ephem.Sun()))
if int(sun_alt) < -3:
   dark = 1
else:
   dark = 0

if int(sun_alt) < -3:
   status = "dark";
if int(sun_alt) > -3 and int(sun_alt) < 5:
      if int(sun_az) > 0 and int(sun_az) < 180:
         status = "dawn"
      else:
         status = "dusk"
if int(sun_alt) >= 5:
   status = "day"


sun_file = open("/home/pi/fireball_camera/sun.txt", "w")
sun_info = "az=" + str(sun_az) + "\n"
sun_info = sun_info + "el=" + str(sun_alt) + "\n"
sun_info = sun_info + "fov=" + str(fov) + "\n"
sun_info = sun_info + "dark=" + str(dark) + "\n"
sun_info = sun_info + "status=" + str(status) + "\n"
sun_file.write(sun_info)


