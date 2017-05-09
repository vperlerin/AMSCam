#!/usr/bin/python3
#from subprocess import call
import os
import requests
from collections import deque
#from queue import Queue
import multiprocessing
import datetime
import cv2
import numpy as np
import iproc 
import time
import syslog
import sys
MORPH_KERNEL = np.ones((10, 10), np.uint8)
record = 1

def cam_loop(pipe_parent):
    #cv2.namedWindow("pepe")
    lc = 0
    tstamp_prev = None
    motion_on = 0
    motion_off = 0
    config = read_config()
    print (config['cam_ip'])

    cap = cv2.VideoCapture("rtsp://" + config['cam_ip'] + "/av0_1&user=admin&password=admin")

    cv2.setUseOptimized(True)
    image_acc = None

    time.sleep(5)
    frames = deque(maxlen=200)
    frame_times = deque(maxlen=200)
    time_start = datetime.datetime.now()
    count = 0
    while True:
        _ , frame = cap.read()
        if _ is True:
            frame_time = datetime.datetime.now()
            frames.appendleft(frame)
            frame_times.appendleft(frame_time)
            #pipe_parent.send(frame)

        if count % 300 == 0:
            time_diff = frame_time - time_start
            fps = count / time_diff.total_seconds()
            print("FPS: " + str(fps))
            count = 1
            lc = lc + 1
            print ("LC:" + str(lc))
            time_start = frame_time

        if count % 3 == 0:
            #alpha = .25
            alpha, tstamp_prev = iproc.getAlpha(tstamp_prev)
            frame = cv2.resize(frame, (0,0), fx=0.25, fy=0.25)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame = cv2.GaussianBlur(frame, (21, 21), 0)
            if image_acc is None:
                image_acc = np.empty(np.shape(frame))
            image_diff = cv2.absdiff(image_acc.astype(frame.dtype), frame,)
            hello = cv2.accumulateWeighted(frame, image_acc, alpha)
            _,threshold = cv2.threshold(image_diff, 30, 255, cv2.THRESH_BINARY)
            thresh= cv2.dilate(threshold, None , iterations=2)
            (_, cnts, xx) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            #cv2.imshow("pepe", frame)
            #cv2.imshow("pepe", image_diff)
            #cv2.waitKey(5)
            if len(cnts) == 0:
               motion_off = motion_off + 1
               print(len(cnts), motion_on, motion_off)
            elif len(cnts) < 30 :
               print(len(cnts), motion_on, motion_off)
               motion_on = motion_on + 1
               motion_off = 0
               #cv2.imshow("pepe", cv2.convertScaleAbs(image_diff))
            else: 
               print ("CNTS:", len(cnts)) 
            if motion_off > 5 and motion_on < 5:
               motion_on = 0
            if lc < 3:
               motion_on = 0
            if motion_off > 10 and motion_on >=5:
               r = requests.get("http://" + config['cam_ip'] + "/webs/btnSettingEx?flag=1000&paramchannel=0&paramcmd=1058&paramctrl=25&paramstep=0&paramreserved=0&")

            if motion_off > 30 and motion_on >= 5: 
               r = requests.get("http://" + config['cam_ip'] + "/webs/btnSettingEx?flag=1000&paramchannel=0&paramcmd=1058&paramctrl=50&paramstep=0&paramreserved=0&")
               print("RECORD BUFFER NOW!\n")
               motion_on = 0
               format_time = frame_time.strftime("%Y%m%d%H%M%S")
               outfile = "{}/{}.avi".format("/var/www/html/out", format_time)
               outfile_text = "{}/{}.txt".format("/var/www/html/out", format_time) 

               df = open(outfile_text, 'w', 1)
               dql = len(frame_times) - 1
               time_diff = frame_times[1] - frame_times[dql]
               fps = 200 / time_diff.total_seconds()
               print ("FPS: ", fps)
               writer = cv2.VideoWriter(outfile, cv2.VideoWriter_fourcc(*'MJPG'), fps, (frames[0].shape[1], frames[0].shape[0]), True)
               while frames:
                   img = frames.pop()
                   ft = frame_times.pop()
                   format_time = ft.strftime("%Y-%m-%d %H:%M:%S.")
                   dec_sec = ft.strftime("%f")
                   format_time = format_time + dec_sec
                   df.write(format_time +"\n")
                   writer.write(img)
                   #i = i + 1
               writer.release()
               df.close()
        count = count + 1

 
def show_loop(pipe_child):
    config = read_config()
    print (config['cam_ip'])

    device_lat = config['device_lat']
    device_lng = config['device_lng']
    device_operator = config['last_name'] + config['first_name']
    device_id= config['device_id']

    image_acc = None
    nice_image_acc = None
    tstamp_prev = None
    count = 0
    #time_start = datetime.datetime.now()
    time_start = time.time()
    frame = pipe_child.recv()
    frames = deque(maxlen=200)
    frame_times = deque(maxlen=200)
    frame_data = deque(maxlen=200)

    motion_on = 0
    motion_off = 0
    cnts = []
    lc = 1
    calibrate_now = 0
    calibrate_start = 0
    #sense_up = 0
 
    while True:
        frame = pipe_child.recv()
        frame_time = time.time()

        frames.appendleft(frame)
        frame_times.appendleft(frame_time)
        
        #frame_info =  str(motion_on) + "|" + str(motion_off) + "|" + str(len(cnts)) + "|"
        #frame_data.appendleft(frame_info)

        #if (count == 0):
            #calibrate on start (only if dark)
            #sys command to sense up
        #    calibrate_start = 1
        #if calibrate_start >= 0:
        #    calibrate_start = calibrate_start + 1

        if (lc % 11 == 0 and count == 5):
            dec_sec = datetime.datetime.fromtimestamp(int(frame_time)).strftime("%f")
            dec_sec_f = dec_sec[:2]
            cframe = frame
            format_time = datetime.datetime.fromtimestamp(int(frame_time)).strftime("%Y-%m-%d %H:%M:%S.")
            cv2.putText(cframe, "AMSMeteors.org / " + device_operator + " " + format_time + dec_sec_f + " UTC " + device_id + " " + device_lat + " " + device_lng,
            (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, .4, (255, 255, 255), 1)
            cv2.imwrite("/var/www/html/out/latest.jpg", cframe)


        if count % 100 == 0:
            time_diff = frame_time - time_start
            #time_diff_seconds = time_diff.total_seconds()
            fps = count / time_diff
            print("FPS: " + str(fps))
            #ff.write("FPS: " + str(fps) + "\n")
            count = 1 
            lc = lc + 1
            print ("LC:" + str(lc))
            time_start = frame_time

        if count % 3 == 0: 
            #if sense_up > 1: 
            #   print ("Sense Up: ", sense_up)
            #if sense_up >= 100 and sense_up < 103:
            #   print ("Take calibration...")
            #   dec_sec = datetime.datetime.fromtimestamp(int(frame_time)).strftime("%f")
            #   dec_sec_f = dec_sec[:2]
            #   cframe = frame
            #   format_time = datetime.datetime.fromtimestamp(int(frame_time)).strftime("%Y-%m-%d %H:%M:%S.")
            #   cv2.putText(cframe, "AMSMeteors.org / " + device_operator + " " + format_time + dec_sec_f + " UTC " + device_id + " " + device_lat + " " + device_lng,
            #   (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, .4, (255, 255, 255), 1)
            #   format_time = datetime.datetime.fromtimestamp(int(frame_time)).strftime("%Y%m%d%H%M%S")
            #   cal_file = "/var/www/html/out/cal" + format_time + ".jpg"
            #   cv2.imwrite(cal_file, cframe)
            #   motion_on = 0 
            #   motion_off = 0 
            #if sense_up == 106:
               #os.system("/var/www/html/write-serial.py sense_down")
            #    print ("Sense down.")
            #   r = requests.get("http://" + config['cam_ip'] + "/webs/btnSettingEx?flag=1000&paramchannel=0&paramcmd=1058&paramctrl=50&paramstep=0&paramreserved=0&")
            #if sense_up > 200: 
            #   calibrate_now = 0
            #   motion_on = 0
            #   motion_on = 0
            #   sense_up = 0



            alpha, tstamp_prev = iproc.getAlpha(tstamp_prev)

            frame = cv2.resize(frame, (0,0), fx=0.8, fy=0.8)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame = cv2.GaussianBlur(frame, (21, 21), 0)
            if image_acc is None:
                image_acc = np.empty(np.shape(frame))
            image_diff = cv2.absdiff(image_acc.astype(frame.dtype), frame,)
            hello = cv2.accumulateWeighted(frame, image_acc, alpha)


            _, threshold = cv2.threshold(image_diff, 30, 255, cv2.THRESH_BINARY)
            thresh= cv2.dilate(threshold, None , iterations=2)
            (_, cnts, xx) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            if len(cnts) == 0:
               motion_off = motion_off + 1
            elif len(cnts) > 2 and lc > 3:
               print ("dropped frame", len(cnts))
               motion_off = motion_off + 1
               dropped = frames.pop()
               #frames.appendleft(last_frame)
            elif lc > 2:
               motion_on = motion_on + 1
               motion_off = 0 
            if motion_off > 5 and motion_on < 3:
               motion_on = 0
            #if calibrate_now == 1:
            #   sense_up = sense_up + 1

            #if motion_off == 3 and motion_on >= 3:
               #r = requests.get("http://" + config['cam_ip'] + "/webs/btnSettingEx?flag=1000&paramchannel=0&paramcmd=1058&paramctrl=25&paramstep=0&paramreserved=0&")

            if motion_off > 20 and motion_on >= 3 and calibrate_now == 0: 
               #ff.write("RECORD BUFFER NOW!\n")
               motion_off = 0
               motion_on = 0
               i = 1000 

               format_time = datetime.datetime.fromtimestamp(int(frame_time)).strftime("%Y%m%d%H%M%S")
               outfile = "{}/{}.avi".format("/var/www/html/out", format_time)
               outfile_text = "{}/{}.txt".format("/var/www/html/out",
               format_time)

               if record == 1: 

                   df = open(outfile_text, 'w', 1)
                   dql = len(frame_times) - 1
                   time_diff = frame_times[1] - frame_times[dql]
                   fps = 200 / time_diff
                   print ("FPS: ", fps) 
                   writer = cv2.VideoWriter(outfile, cv2.VideoWriter_fourcc(*'MJPG'), fps, (frames[0].shape[1], frames[0].shape[0]), True)
                   while frames:
                       img = frames.pop()
                       ft = frame_times.pop()
                       format_time = datetime.datetime.fromtimestamp(int(ft)).strftime("%Y-%m-%d %H:%M:%S.")
                       dec_sec = datetime.datetime.fromtimestamp(int(frame_time)).strftime("%f")
                       format_time = format_time + dec_sec
                       #img_data  = frame_data.pop()
                       #fts = ft.strftime("%Y%m%d %H:%M:%S.%f|")
                       df.write(format_time +"\n")
                       #cv2.putText(img, img_time.strftime("AMSMeteors.org / " + device_operator + " %Y%m%d %H:%M:%S." + dec_sec_f + " UTC " + device_id + ": " + device_lat + " " + device_lng),
                       #(10, img.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, .5, (255, 255, 255), 1)
                       #cv2.imwrite("out/" + str(i) + ".jpg", img)
                       writer.write(img)
                       i = i + 1
                   writer.release()
                   df.close()
                   #r = requests.get("http://" + config['cam_ip'] + "/webs/btnSettingEx?flag=1000&paramchannel=0&paramcmd=1058&paramctrl=50&paramstep=0&paramreserved=0&")
                   #calibrate_now = 1
                   #sense_up = sense_up + 1

            if motion_on > 0:
                #ff.write("motion_on " + str(motion_on) + "\n")
                print("motion_on " + str(motion_on) + "\n")
            #cv2.imshow('pepe', frame)

        #last_frame = frame
        count = count + 1

def read_config():
    config = {}
    file = open("config.txt", "r")
    for line in file:
      line = line.strip('\n')
      data = line.rsplit("=",2)
      config[data[0]] = data[1]
      #print key, value
    return(config)




 
def write_buffer(frames):
    print ("YA, write")
    for i in range(len(frames), 0, -1):
         print (i)
         frames[i-0]



if __name__ == '__main__':
 
    print ("Capture Program")
    #logger = multiprocessing.log_to_stderr()
    #logger.setLevel(multiprocessing.SUBDEBUG)
 
    pipe_parent, pipe_child = multiprocessing.Pipe()
 
    cam_process = multiprocessing.Process(target=cam_loop,args=(pipe_parent, ))
    cam_process.start()
 
    #show_process = multiprocessing.Process(target=show_loop,args=(pipe_child, ))
    #show_process.start()

    cam_process.join()
    show_loop.join()
