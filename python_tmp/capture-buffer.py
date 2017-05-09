#!/usr/bin/python3
#from subprocess import call
from pathlib import Path
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

    cap = cv2.VideoCapture("rtsp://" + config['cam_ip'] + "/av0_0&user=admin&password=admin")

    cv2.setUseOptimized(True)
    image_acc = None

    time.sleep(5)
    frames = deque(maxlen=200)
    frame_times = deque(maxlen=200)
    time_start = datetime.datetime.now()
    count = 0
    record = 0
    while True:
        _ , frame = cap.read()
        if _ is True:
            frame_time = datetime.datetime.now()
            frames.appendleft(frame)
            frame_times.appendleft(frame_time)
            #pipe_parent.send(frame)

            write_alert = Path("/home/pi/fireball_camera/write_buffer");
            if (write_alert.is_file()):
                record = 1
            else:
                record = 0

            if record == 1:
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
