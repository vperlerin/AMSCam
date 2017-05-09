# amsaware
# This script checks for AMS Fireball events and reports and 
# checks the recordings of this device to see if the event was 
# capture. If video files exist around the time of the event
# the files will be uploaded to the AMS for further analysis. 

import sys
import os
import time as gtime
from os import listdir
from os.path import isfile, join 
import json, requests
import numpy as np
from datetime import datetime, date, time
from dateutil import parser

def read_files(dir):
    captures = [f for f in listdir(dir) if isfile(join(dir, f))]
    return(captures)

def read_config():
    config = {}
    file = open("config.txt", "r")
    for line in file:
      line = line.strip('\n')
      data = line.rsplit("=",2)
      config[data[0]] = data[1]
    return(config)

def read_fov():
    lats = []
    lons = []
    file = open("fov.txt")
    for line in file:
       (lon,lat,alt) = line.split(",")
       lats.append(float(lat))
       lons.append(float(lon))
    max_lat = max(lats)
    max_lon = max(lons)
    min_lat = min(lats)
    min_lon = min(lons)
    return(max_lat, max_lon, min_lat, min_lon)

def get_ams_reports(ams_year, ams_event_id,type, ratings):
   api_key = "QwCsPJKr87y15Sy"
   url = "http://www.amsmeteors.org/members/api/open_api/get_reports_for_event"
   data = {'api_key' : api_key, 'year' : ams_year, 'event_id' : ams_event_id, 'format' : 'json', 'override' : 0, 'ratings' : ratings}
   r = requests.get(url, params=data)
   dates = []
   my_data = r.json()
   data = json.loads(r.text)
   #print data
   for key in data['result']:
      ams_witness_id = data['result'][key]['report_id']
      dt = data['result'][key]['report_date_utc']
      record_date = data['result'][key]['report_date_utc']
      lat = data['result'][key]['latitude']
      lon = data['result'][key]['longitude']
      alt = data['result'][key]['altitude']
      az1 = data['result'][key]['initial_azimuth']
      el1 = data['result'][key]['initial_altitude']
      az2 = data['result'][key]['final_azimuth']
      el2 = data['result'][key]['final_altitude']
      wr = data['result'][key]['rating']
      if type == 'detail':
         if wr >= ratings:
            print (ams_witness_id + "|" + dt + "|" + record_date + "|" + lat + "|" + lon + "|" + alt + "|" + az1 + "|" + el1 + "|" + az2 + "|" + el2 + "|")
      dates.append(dt)

   if (type == 'datetime'):
      return(dates)

def avg_dates (avg_date_utc, datetimes):
   good_datetimes = []
   good_avg_date = parser.parse(avg_date_utc)
   for dts in datetimes:
      dt = parser.parse(dts)
      time_diff = dt - good_avg_date
      minutes, seconds = divmod(time_diff.total_seconds(), 60)
      if minutes < 20 and minutes > -20:
         good_datetimes.append(dt)

   avg_date = datetime.date(good_avg_date)

   total = sum(dt.hour * 3600 + dt.minute * 60 + dt.second for dt in good_datetimes)
   avg = total / len(datetimes)
   minutes, seconds = divmod(int(avg), 60)
   hours, minutes = divmod(minutes, 60)
   return datetime.combine(date(avg_date.year, avg_date.month, avg_date.day), time(hours, minutes, seconds))

def get_ams_event(year, event_id, ratings):
   num_reports = 0
   api_key = "QwCsPJKr87y15Sy"
   url = "http://www.amsmeteors.org/members/api/open_api/get_event"
   data = {'api_key' : api_key, 'year' : year, 'event_id' : event_id, 'format' : 'json', 'ratings': ratings, 'override': 0}
   r = requests.get(url, params=data)
   my_data = r.json()
   if "result" not in my_data.keys():
      print ("No trajectory for this event.")
      return(0)
   #try:
   #   event_datetime_utc = my_data['result'][event_key]['avg_date_utc']
   #except:
   #   print ("No trajectory for this event.")
   #   return(0)
   
   event_key = "Event #" + str(event_id) + "-" + str(year)
   event_datetime_utc = my_data['result'][event_key]['avg_date_utc']
   fb_start_lat =  my_data['result'][event_key]['start_lat']
   fb_start_lon =  my_data['result'][event_key]['start_long']
   fb_start_alt =  my_data['result'][event_key]['start_alt']
   fb_end_lat =  my_data['result'][event_key]['end_lat']
   fb_end_lon =  my_data['result'][event_key]['end_long']
   fb_end_alt =  my_data['result'][event_key]['end_alt']
   impact_lat = my_data['result'][event_key]['impact_lat'];
   impact_lon = my_data['result'][event_key]['impact_long']
   (num_reports, xxx) =my_data['result'][event_key]['num_reports_for_options'].split("/")
   epicenter_lon = my_data['result'][event_key]['epicenter_long']
   epicenter_lat = my_data['result'][event_key]['epicenter_lat']

   # REFINE THE DATE
   type = 'datetime'
   dates = get_ams_reports(year, event_id, type, ratings)
   if len(dates) > 0:
      better_event_datetime =  avg_dates(event_datetime_utc, dates)

   # PRINT EVENT DETAILS
   print ("Average Event Datetime: \t" + event_datetime_utc)
   #if len(dates) > 0:
      #print ("Better Average Datetime:\t" + better_event_datetime.strftime("%Y-%m-%d %H:%M:%S"))
   #print ("Fireball Start Lat/Lon/Alt:\t" + str(fb_start_lat) + "/" + str(fb_start_lon) + "/" + str(fb_start_alt))
   #print ("Fireball End Lat/Lon/Alt:\t" + str(fb_end_lat) + "/" + str(fb_end_lon) + "/" + str(fb_end_alt))
   #print ("Impact Lat/Lon/Alt:      \t" + str(impact_lat) + "/" + str(impact_lon) + "/0")
   #print ("Event Epicenter Lat/Lon:\t" + str(epicenter_lat) + "/" + str(epicenter_lon))
   #print ("Camera FOV Max Lat/Lon:\t\t" + str(max_lat) + "/" + str(max_lon))
   #print ("Camera FOV Min Lat/Lon:\t\t" + str(min_lat) + "/" + str(min_lon))

   if fb_start_lat >= min_lat and fb_start_lat <= max_lat:
       start_lat_match = 1
   else:
       start_lat_match = 0
   if fb_start_lon >= min_lon and fb_start_lon <= max_lon:
       start_lon_match = 1
   else:
       start_lon_match = 0

   if fb_end_lat >= min_lat and fb_end_lat <= max_lat:
       end_lat_match = 1
   else:
       end_lat_match = 0
   if fb_end_lon >= min_lon and fb_end_lon <= max_lon:
       end_lon_match = 1
   else:
       end_lon_match = 0

   print ("Start Point in FOV:\t\t", start_lat_match, start_lon_match)
   print ("End Point in FOV:\t\t", end_lat_match, end_lon_match)
   return(better_event_datetime)

def get_close_events(start_date, end_date, lat, lon,  max_lat, max_lon, min_lat, min_lon):

   events = set() 
   event_dates = {} 
   api_key = "QwCsPJKr87y15Sy"
   url = "http://www.amsmeteors.org/members/api/open_api/get_close_reports"
   data = {'api_key' : api_key, 'start_date' : start_date, 'end_date' : end_date, 'lat': lat, 'lng': lon, 'format' : 'json'}
   print (data)
   r = requests.get(url, params=data)
   my_data = r.json()
   #print my_data

   if "result" not in my_data.keys():
      print ("No close events.")
      exit()

   for row in my_data['result']:
       #print (str(row), str(my_data['result'][row]['latitude']), str(my_data['result'][row]['longitude']), str(my_data['result'][row]['report_date_utc']))
       if "#" in str(row):
           (a, b, c) = str(row).split(" ")
           (utc_date) = my_data['result'][row]['report_date_utc']
           (event_id, year) = b.split("-", 2)
           event_id = event_id.replace("#", "")
           event_id = int(event_id)
           events.add(event_id)
           event_dates[event_id] = utc_date 
       else: 
           print ("skip pending report")   

   captures = read_files("/var/www/html/out")
   print ("Unique events within your area.")
   for event_id in events:
       print ("Event ID:\t\t\t" + str(event_id))
       avg_date = get_ams_event(year, event_id, 1)
       if avg_date == 0:
          avg_date = parser.parse(event_dates[event_id])
       # compare dates on files here
       print ("Looking for files near this date:", avg_date)
       for capture in captures:
           if "avi" in capture:
              #print (capture, avg_date)
              (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat("/var/www/html/out/" + capture)
              

              file_date = datetime.strptime(gtime.ctime(ctime), "%a %b %d %H:%M:%S %Y")
              time_diff = avg_date - file_date

              #time_diff = dt - good_avg_date
              minutes, seconds = divmod(time_diff.total_seconds(), 60)
              if minutes > -180 and minutes < 180:
                 print (minutes, capture, avg_date, gtime.ctime(ctime))

check_date = sys.argv[1]

(max_lat, max_lon, min_lat, min_lon) = read_fov()
config = read_config()
get_close_events(check_date + " 00:00:00", check_date + ' 23:59:59', config['device_lat'], config['device_lng'], max_lat, max_lon, min_lat, min_lon)
