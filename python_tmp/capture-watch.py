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

    #cv2.setUseOptimized(True)
    image_acc = None

    time.sleep(5)
    frames = deque(maxlen=200)
    frame_times = deque(maxlen=200)
    time_start = datetime.datetime.now()
    count = 0
    while True:
        _ , frame = cap.read()
        #if _ is True:
        #    frame_time = datetime.datetime.now()
        #    frames.appendleft(frame)
        #    frame_times.appendleft(frame_time)
        #    #pipe_parent.send(frame)

        if True:
            #alpha = .25
            alpha, tstamp_prev = iproc.getAlpha(tstamp_prev)
            #frame = cv2.resize(frame, (0,0), fx=0.25, fy=0.25)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame = cv2.GaussianBlur(frame, (21, 21), 0)
            if image_acc is None:
                image_acc = np.empty(np.shape(frame))
            image_diff = cv2.absdiff(image_acc.astype(frame.dtype), frame,)
            hello = cv2.accumulateWeighted(frame, image_acc, alpha)
            _,threshold = cv2.threshold(image_diff, 30, 255, cv2.THRESH_BINARY)
            thresh= cv2.dilate(threshold, None , iterations=2)
            (_, cnts, xx) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if len(cnts) == 0:
               motion_off = motion_off + 1
            elif len(cnts) < 30 :
               motion_on = motion_on + 1
               motion_off = 0
               print (len(cnts), motion_on)
            if motion_off > 3 and motion_on < 3:
               motion_on = 0
            if count < 100:
               motion_on = 0
            #if motion_off > 10 and motion_on >=5:
            #   r = requests.get("http://" + config['cam_ip'] + "/webs/btnSettingEx?flag=1000&paramchannel=0&paramcmd=1058&paramctrl=25&paramstep=0&paramreserved=0&")

            if motion_off > 10 and motion_on >= 3: 
            #   r = requests.get("http://" + config['cam_ip'] + "/webs/btnSettingEx?flag=1000&paramchannel=0&paramcmd=1058&paramctrl=50&paramstep=0&paramreserved=0&")
               print("RECORD BUFFER NOW!\n")
               os.system("touch /home/pi/fireball_camera/write_buffer");
               time.sleep(2)
               os.system("rm /home/pi/fireball_camera/write_buffer");
               motion_on = 0
               #motion_off = 0
               count = 0
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
