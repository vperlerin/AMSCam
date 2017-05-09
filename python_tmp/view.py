#!/usr/bin/python3 
import requests
import pytesseract
from io import BytesIO
from pathlib import Path
import glob
import collections
from collections import deque
from PIL import Image, ImageChops
from queue import Queue
import multiprocessing
import datetime
import cv2
import numpy as np
import iproc 
import time
import ephem
import sys
import os
from amscommon import read_config, caldate
#from wand.image import Image
#from wand.display import display

MORPH_KERNEL       = np.ones((10, 10), np.uint8)

def log_fireball_event(config, maybe_file, maybe_summary_file, maybe_object_file, values) :
   url = "http://www.amsmeteors.org/members/api/cam_api/log_fireball_event"
   _data = {
    'api_key': config['api_key'],
    'device_id': config['device_id'],
    'datetime': values['datetime'],
    'motion_frames' : values['motion_frames'],
    'cons_motion': values['cons_motion'],
    'color' : int(values['color']),
    'straight_line' : values['straight_line'],
    'bp_frames' : values['bp_frames'],
    'format': 'json',
    'meteor_yn': values['meteor_yn'] 
   }


   summary = maybe_summary_file.replace("-summary", "")
   os.system("mv " + maybe_summary_file + " " + summary)
   print("mv " + maybe_summary_file + " " + summary)

   event_stack = maybe_object_file.replace("-objects", "")
   event = maybe_file
   #time.sleep(1)
   os.system("cat " + summary + "> /tmp/sum.txt")
 
   _files = {'event_stack': open(event_stack, 'rb'), 'event':open(event, 'rb'), 'summary':open(summary, 'r') }

   print ("Summary TXT: ", summary)
   session = requests.Session()
   del session.headers['User-Agent']
   del session.headers['Accept-Encoding']

   with requests.Session() as session:
      response = session.post(url, data= _data, files=_files)

   print (response.text)
   response.raw.close()

def log_motion_capture(config, file, values):
   stack_file = file.replace("-objects", "")
   os.system("cp " + file + " " + stack_file)
   url = "http://www.amsmeteors.org/members/api/cam_api/log_motion_capture"
   _files = {'event_stack': open(stack_file, 'rb')}
   _data = {
    'api_key': config['api_key'],
    'device_id': config['device_id'],
    'datetime': values['datetime'],
    'motion_frames' : values['motion_frames'],
    'cons_motion': values['cons_motion'],
    'color' : int(values['color']),
    'straight_line' : values['straight_line'],
    'bp_frames' : values['bp_frames'],
    'format': 'json',
    'meteor_yn': values['meteor_yn'] 
   }
   session = requests.Session()
   del session.headers['User-Agent']
   del session.headers['Accept-Encoding']

   with requests.Session() as session:
      response = session.post(url, data= _data, files=_files)

   print (response.text)
   response.raw.close() 

def day_or_night(file):

   year = file[0:4]
   month = file[4:6]
   day = file[6:8]
   hour = file[8:10]
   min = file[10:12]
   sec = file[12:14]
   date_str = year + "/" + month + "/" + day + " " + hour + ":" + min
   print("File:", file)
   print(year,month,day,hour,min,sec)
   config = read_config()
   obs = ephem.Observer()
   obs.pressure = 0
   obs.horizon = '-0:34'
   obs.lat = config['device_lat']
   obs.lon = config['device_lng']
   #cur_date = time.strftime("%Y/%m/%d %H:%M")
   cur_date = datetime.datetime.strptime(date_str, "%Y/%m/%d %H:%M")
   obs.date = cur_date
   print ("FILE DATE: ", cur_date)
   sun = ephem.Sun()
   sun.compute(obs)
   if sun.alt > -10:
      status = "day"
   else:
      status = "night"

   #print (obs.lat, obs.lon, obs.date)
   #print ("Sun Alt: %s, Sun AZ: %s" % (sun.alt, sun.az))
   (sun_alt, x,y) = str(sun.alt).split(":")
   (sun_az, x,y) = str(sun.az).split(":")
   print ("Sun Alt: %s" % (sun_alt))
   if int(sun_alt) < -10:
      status = "dark";
   if int(sun_alt) >- 10 and int(sun_alt) < 5:
      if int(sun_az) > 0 and int(sun_az) < 180:
         status = "dawn"
      else:
         status = "dusk"
   if int(sun_alt) >= 5:
      status = "day";

   return(status)


def analyze(file):
    config = read_config()
    a = 0
    b = 0
    bright_pixel_count = 0
    bright_pixel_total = 0
    elapsed_frames = 0
    cons_motion = 0
    straight_line = 100
    straight = 'N'
    motion = 0
    motion_off = 0
    frame_data = {}
    data_file = file.replace(".avi", ".txt");
    summary_file = data_file.replace(".txt", "-summary.txt")
    object_file = data_file.replace(".txt", "-objects.jpg")
    fp = open(data_file, "r")
    sfp = open(summary_file, "w")
    event_start_frame = 0
    event_end_frame = 0
    sum_color = 0
    cons_motion = 1 
    max_cons_motion = 0
    cons_motion_events = 0
    last_motion = 0
    mid_pix_count = 0
    for line in fp:
       (frame,contours,area,perimeter,convex,x,y,w,h,middle_pixel,n) = line.split("|")
       if (middle_pixel== ""):
          middle_pixel= 0
       if frame != 'frame':
          if contours != "":
             motion = motion + 1
             motion_off = 0
             if last_motion > 0:
                cons_motion = cons_motion + 1
             if cons_motion > max_cons_motion:
                max_cons_motion = cons_motion
          if motion < 5  and contours == "":
             motion = 0
             last_motion = 0
             cons_motion = 0
          if motion == 5 and event_start_frame == 0:
             event_start_frame = int(frame) 
          if motion >= 1 and contours == "":
             motion_off = motion_off + 1
          if motion > 5 and motion_off > 5 and event_end_frame == 0:
             event_end_frame = int(frame) - 5 
          if int(middle_pixel) > 0:
             sum_color = sum_color + int(middle_pixel)
             mid_pix_count = mid_pix_count + 1
             if int(middle_pixel) >= 180:
                print ("Bright Pixel Count/Mid Pix Total", bright_pixel_count, middle_pixel)
                bright_pixel_count = bright_pixel_count + 1
                bright_pixel_total = bright_pixel_total + int(middle_pixel)


          out = str(frame)+","+str(contours)+","+str(area)+","+str(perimeter)+","+str(convex)+","+str(x) + "," + str(y) + "," + str(w) + "," + str(h) + "," + str(middle_pixel) + "," + str(n) + ",\n"
          frame_data.update({int(frame) : {'x': x, 'y': y}})
          sfp.write(out)
          cons_motion = motion
          print(out)
          if (event_start_frame != 0 and event_end_frame == 0 and middle_pixel != ""):
             #print ("COLOR:", color)
             last_frame_motion = motion
             last_frame_cnts = contours 
    out = "Event Start Frame : " + str(event_start_frame) + "\n"
    sfp.write(out)
    print (out)
    out = "Event End Frame : " + str(event_end_frame) + "\n"
    sfp.write(out)
    print (out)
    if (bright_pixel_count > 0):
       out = "Bright Frames: " + str(bright_pixel_count) + "\n"
       sfp.write(out)
       print (out)
       out = "Bright Frame Avg: " + str(bright_pixel_total/bright_pixel_count) + "\n"
       sfp.write(out)
       print (out)
    sfp.write(out)
    print (out)

    key_frame1 = int(event_start_frame)
    key_frame2 = int(event_start_frame + ((int(event_end_frame - event_start_frame) / 2)))
    key_frame3 = int(event_end_frame - 3)
    ofr = collections.OrderedDict(sorted(frame_data.items()))

    out = "Key Frames: " + str(key_frame1) + "," + str(key_frame2) + "," + str(key_frame3) + "\n"
    sfp.write(out)
    print (out)
    elapsed_frames = key_frame3 - key_frame1
    if cons_motion > 0 and mid_pix_count > 0:
       avg_center_pixel = int(sum_color) / mid_pix_count
    else:
       avg_center_pixel = 0
    out = "Sum Color/Frames: " + str(sum_color) + "/" + str(mid_pix_count) + "\n"
    sfp.write(out)
    print (out)
    out = "Consectutive Motion Frames: " + str(max_cons_motion) + "\n"
    sfp.write(out)
    print (out)
    if max_cons_motion > 10 and event_end_frame > 0 and 'x' in frame_data[key_frame3] and 'x' in frame_data[key_frame2] and 'x' in frame_data[key_frame1]:
       if ( frame_data[key_frame1]['x'] != '' and frame_data[key_frame2]['x'] != '' and frame_data[key_frame3]['x'] != '' ):
          x1 = int(frame_data[key_frame1]['x'])
          y1 = int(frame_data[key_frame1]['y'])
          #print("X2: ", frame_data[key_frame2]['x'])
          x2 = int(frame_data[key_frame2]['x'])
          y2 = int(frame_data[key_frame2]['y'])
          x3 = int(frame_data[key_frame3]['x'])
          y3 = int(frame_data[key_frame3]['y'])

          if x2 - x1 != 0:
             a = (y2 - y1) / (x2 - x1)
          if x3 - x1 != 0:
             b = (y3 - y1) / (x3 - x1)
          straight_line = a - b
          if (straight_line < 1):
             straight = "Y" 
    else: 
       out = "Not enough consecutive motion."
       sfp.write(out)
       print (out)
       
    meteor = "N"
    if (straight_line < 1 and avg_center_pixel > 40 or (bright_pixel_count > 10 )):
       meteor = "Y"
    sfp.write("Elapsed Frames:\t" + str(elapsed_frames)+ "\n")
    print("Elapsed Frames:\t" + str(elapsed_frames)+ "\n")
    sfp.write("Straight Line:\t" + str(straight) + "," + str(straight_line)+"\n")
    print("Straight Line:\t" + str(straight) + "," + str(straight_line)+"\n")
    sfp.write("Average Center Pixel Color:\t" + str(avg_center_pixel) + "\n")
    print("Average Center Pixel Color:\t" + str(avg_center_pixel) + "\n")
    sfp.write("Likely Meteor:\t"+ str(meteor)+"\n")
    print("Likely Meteor:\t"+ str(meteor)+"\n")
    fp.close()
    sfp.close()
    if meteor == "N":
       false_file= file.replace("out/", "out/false/")
       false_data_file= data_file.replace("out/", "out/false/")
       false_summary_file= summary_file.replace("out/", "out/false/")
       false_object_file = object_file.replace("out/", "out/false/")
       cmd = "mv " + file + " " + false_file 
       os.system(cmd)
       cmd = "mv " + data_file + " " + false_data_file
       os.system(cmd)

       cmd = "mv " + summary_file + " " + false_summary_file
       print ("SUMMARY FILE CMD", cmd)
       os.system(cmd)

       cmd = "mv " + object_file + " " + false_object_file
       os.system(cmd)
       el = false_object_file.split("/")
       motion_date = caldate(el[-1])
       values = {
          'datetime': motion_date,
          'motion_frames' : elapsed_frames,
          'cons_motion': max_cons_motion,
          'color' : avg_center_pixel,
          'straight_line' : straight_line,
          'bp_frames' : bright_pixel_count,
          'meteor_yn': meteor
       }
       log_motion_capture(config, false_object_file, values) 
    else:  
       maybe_file= file.replace("out/", "out/maybe/")
       maybe_data_file= data_file.replace("out/", "out/maybe/")
       maybe_summary_file= summary_file.replace("out/", "out/maybe/")
       cmd = "mv " + file + " " + maybe_file 
       maybe_object_file = object_file.replace("out/", "out/maybe/")
       os.system(cmd)
       cmd = "mv " + data_file + " " + maybe_data_file
       os.system(cmd)
       cmd = "mv " + summary_file + " " + maybe_summary_file
       print (cmd)
       os.system(cmd)
       cmd = "mv " + object_file + " " + maybe_object_file
       os.system(cmd)
       cmd = "./astr-stack.py " + maybe_file
       print (cmd)
       os.system(cmd)


       el = maybe_object_file.split("/")
       motion_date = caldate(el[-1])
       values = {
          'datetime': motion_date,
          'best_calibration' : config['best_caldate'],
          'motion_frames' : elapsed_frames,
          'cons_motion': max_cons_motion,
          'color' : avg_center_pixel,
          'straight_line' : straight_line,
          'bp_frames' : bright_pixel_count,
          'meteor_yn': meteor
       }
       

       log_fireball_event(config, maybe_file, maybe_summary_file, maybe_object_file, values) 

  
def view(file, show):
    stk_img = None
    jpg = file
    data_file = file
    jpg = jpg.replace(".avi", ".jpg");
    jpg = jpg.replace("out", "jpgs");
    data_file = data_file.replace(".avi", ".txt");
    object_file = data_file.replace(".txt", "-objects.jpg")

    cap = cv2.VideoCapture(file)
    final_cv_image = None
    time.sleep(2)

    tstamp_prev = None
    image_acc = None
    last_frame = None
    nice_image_acc = None
    final_image = None
    cur_image = None
    if show == 1:
       cv2.namedWindow('pepe')
    count = 0
    frames = deque(maxlen=256)
    out_jpg = np.zeros((500,500,3))
    out_jpg_final = np.zeros((500,500,3))
    oy = 0
    ox = 0
    max_h = 0
    fp = open(data_file, "w")
    fp.write("frame|contours|area|perimeter|convex|x|y|w|h|color|\n")
    mid_pix_total = 0
    mid_pix_count = 0
    while True:
        frame_file = jpg.replace(".jpg", "-" + str(count) + ".jpg");
        _ , frame = cap.read()
        #cv2.imwrite(frame_file, frame)
        if frame is None:
           if count == 0:
               print ("bad file!")
               return()
           #print (jpg)
           #cv2.imwrite(jpg, final_cv_image)
           if max_h <= 500:
              out_jpg_final = out_jpg[0:max_h,0:500]
           else: 
              out_jpg_final = out_jpg[0:500,0:500]
           if max_h > 0:
              #stack_frame /= count * .25
              print ("Writing Object File", object_file)
              cv2.imwrite(object_file, stack_frame)
              #cv2.imwrite(object_file, out_jpg_final)
           else: 
              #stack_frame /= count * .25
              #cv2.imwrite(object_file, out_jpg)
              cv2.imwrite(object_file, stack_frame)
              print ("Writing Object File", object_file)
           return()
           #exit()

#        frames.appendleft(frame)

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        nice_frame = frame
        if count == 0:
           stack_frame = gray_frame 

        alpha, tstamp_prev = iproc.getAlpha(tstamp_prev)
        #print ("ALPHA: ", alpha)
        #frame = cv2.resize(frame, (0,0), fx=0.8, fy=0.8)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = cv2.GaussianBlur(frame, (21, 21), 0)
        if last_frame is None:
            last_frame = nice_frame 
        if image_acc is None:
            image_acc = np.empty(np.shape(frame))
        image_diff = cv2.absdiff(image_acc.astype(frame.dtype), frame,)
        hello = cv2.accumulateWeighted(frame, image_acc, alpha)
        _, threshold = cv2.threshold(image_diff, 30, 255, cv2.THRESH_BINARY)
        thresh= cv2.dilate(threshold, None , iterations=2)
        (_, cnts, xx) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        data = str(count) + "|" 
        if len(cnts) > 0:

            image_diff_nice = cv2.absdiff(last_frame.astype(last_frame.dtype), nice_frame,)
            _, threshold = cv2.threshold(image_diff, 30, 255, cv2.THRESH_BINARY)
            thresh= cv2.dilate(threshold, None , iterations=2)
            (_, alt_cnts, xx) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if len(alt_cnts) != 0:
               cnts = alt_cnts

            area = cv2.contourArea(cnts[0])
            perim = cv2.arcLength(cnts[0], True)
            #print ("Perim:", perim)
            #for cnt in cnts:
            x,y,w,h = cv2.boundingRect(cnts[0])
               

            #ellipse = cv2.fitEllipse(cnts[0])
            #print ("Ellipse:", len(ellipse), ellipse)
            #if len(ellipse) == 5:
            #   cv2.ellipse(frame,ellipse,(0,255,0),2)


            #if count % 20 == 0:
            #   for cnt in cnts:
                  # crop out
            x,y,w,h = cv2.boundingRect(cnts[0])
            x2 = x+w
            y2 = y+h
            mx = int(x + (w/2))
            my = int(y + (h/2))
            crop_frame = gray_frame[y:y2,x:x2]
            stack_frame[y:y2,x:x2] = crop_frame 
                  #   stack_frame[...,0] = np.clip(stack_frame[...,0], 0, 255)
                  #   print (stack_frame[y:y2,x:x2])
 
            #print ("XY:", x,x2,y,y2)

            middle_pixel = gray_frame[my,mx]
            middle_sum = np.sum(middle_pixel)
            #print("MID PIX:", middle_pixel, middle_sum)
            mid_pix_total = mid_pix_total + middle_pixel
            mid_pix_count = mid_pix_count + 1
            #cv2.circle(nice_frame,(mx,my),5,(255,0,0))
            cy = (y + y2) / 2
            cx = (x + x2) / 2 
            #stack_frame[y:y2,x:x2] = crop_frame 
            #if stk_img is None :
            #   stk_img = Image.fromarray(stack_frame)
            #   last_stk_img = Image.fromarray(stack_frame)
            #else:
            #   stk_img = Image.fromarray(nice_frame)
            #   stk_img = Image.blend(stk_img, last_stk_img, .95) 
            #   last_stk_img = stk_img 
            #stack_frame += image_diff_nice
            #display(stk_img)
            #if count % 10 == 0:
            #   stk_img.show()
            text = (pytesseract.image_to_string(Image.fromarray(crop_frame)))
            print (text)
            if h > max_h and h < 300:
               max_h = h
               print ("MAX Height Hit", max_h)

            if (ox + w) < 500 and (oy + h) < 500 and len(text) == 0:
               print ("OY,OY+H,OX,OX+W,color,cnts: ", oy, oy+h, ox, ox+w, middle_pixel, len(cnts))
               try: 
                  out_jpg[oy:oy+h,ox:ox+w] = crop_frame
               except:
                  print("crop too big for summary!")
               #if show == 1:
                  #cv2.imshow('pepe', cv2.convertScaleAbs(stack_frame))
                  #cv2.imshow('pepe', stack_frame)
                  #cv2.waitKey(1) 
               ox = ox +w
            else: 
               print("Crop to big for summary pic!", oy,oy+h,ox,ox+w,h,w)
               time.sleep(5)
            if (ox + w ) >= 500 and (w < 400):
               oy += max_h
               ox = 0  


            avg_color_per_row = np.average(crop_frame, axis=0)
            avg_color = np.average(avg_color_per_row, axis=0)
            #print ("AVG COLOR: " , avg_color, np.sum(avg_color))
            tjpg = jpg
            tjpg = tjpg.replace(".jpg", "-" + str(count) + ".jpg")
           # print ("TJPG", tjpg)
            #cv2.imwrite(tjpg, crop_frame)
            #cv2.imwrite(tjpg, stack_frame)


            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,255,255),1)

            poly = cv2.approxPolyDP(cnts[0], 0.02*perim, True)

            #print ("Poly: ", poly)
            #print ("Convex?: ", cv2.isContourConvex(cnts[0]))
            convex = cv2.isContourConvex(cnts[0])
            #data = "frame|contours|area|perimeter|poly|convex|x|y|w|h|color|\n" 
            data = data + str(len(cnts)) + "|" + str(area) + "|" + str(perim) + "|"
            #data = data + str(poly) + "|"
            data = data + str(convex) + "|"
            data = data + str(x) + "|"
            data = data + str(y) + "|"
            data = data + str(w) + "|"
            data = data + str(h) + "|"
            data = data + str(middle_pixel) + "|"
        else:
            data = data + "|||||||||"
        fp.write(data + "\n")
    
        last_frame = nice_frame 



        #nice_avg = cv2.convertScaleAbs(nice_image_acc)

        #print (cnts)


        #if cur_image is None:
        #    cur_image = Image.fromarray(frame)

            #temp = cv2.convertScaleAbs(nice_image_acc)
            #nice_image_acc_pil = Image.fromarray(temp)
            #cur_image = ImageChops.lighter(cur_image, nice_image_acc_pil)

        #final_cv_image = np.array(cur_image)
        #cv2.imshow('pepe', final_cv_image)
        #if count % 1 == 0:
        #    cv2.imshow('pepe', frame)
        count = count + 1
        #print (count)
        #cv2.waitKey(1)

try: 
   file = sys.argv[1]
   batch = 0
except:
   files = glob.glob("/var/www/html/out/*.avi") 
   batch = 1

if batch == 0:
   status = day_or_night(file)
   print ("This video was taken during: ", status)
   view("/var/www/html/out/" + file, 1)
   analyze("/var/www/html/out/" + file)
else:
   for file in files:
      file = file.replace("/var/www/html/out/", "")
      print (file)  
      view("/var/www/html/out/" + file, 0)
      analyze("/var/www/html/out/" + file)


