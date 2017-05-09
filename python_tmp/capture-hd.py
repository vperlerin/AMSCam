#!/usr/bin/python3
#from subprocess import call
import numpy as np
print (np.__path__)
print (np.__version__)
from pathlib import Path
import os
import requests
from collections import deque
#from queue import Queue
import multiprocessing
#from multiprocessing import Process, Manager
from amscommon import read_config
import datetime
import cv2
import iproc 
import time
import syslog
import sys
MORPH_KERNEL = np.ones((10, 10), np.uint8)
record = 1


def cam_loop(pipe_parent, shared_dict):
    lc = 0
    tstamp_prev = None
    motion_on = 0
    motion_off = 0
    config = read_config()
    print (config['cam_ip'])


    if int(config['hd']) == 1:
        print ("capture_hd")
        cap = cv2.VideoCapture("rtsp://" + config['cam_ip'] + "/av0_0&user=admin&password=admin&tcp")
        resize = .25
    else:
        cap = cv2.VideoCapture("rtsp://" + config['cam_ip'] + "/av0_1&user=admin&password=admin&tcp")
        resize = .5 

    cv2.setUseOptimized(True)
    image_acc = None
    time_start = datetime.datetime.now()

    log = open("/var/www/html/out/log.txt", "w")
    log.write("Capture Process Started: " + time_start.strftime("%Y%m%d%H%M%S"))

    time.sleep(7)
    frames = deque(maxlen=200)
    frame_times = deque(maxlen=200)
    #frame_data = deque(maxlen=200)
    count = 0
    shared_dict['motion_on'] = 0
    shared_dict['motion_off'] = 0

    cap_start_unix_time = time.time()
    start_frame_time = cap.get(0)
    cap_unix_time = cap_start_unix_time + (start_frame_time / 1000)

    while True:
        _ , frame = cap.read()
        if _ is True:
            currentFrame = cap.get(0)
            this_time = time.time()
            cap_unix_time = cap_start_unix_time + (currentFrame/ 1000)
            latency = this_time - cap_unix_time
            print (this_time, cap_unix_time, latency)

            #if int(config['hd']) == 0:
            #    frame = cv2.resize(frame, (0,0), fx=1, fy=.75)
            frame_time = datetime.datetime.now()
            frames.appendleft(frame)
            frame_times.appendleft(frame_time)
        if count % 5 == 0:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            pipe_parent.send(cv2.resize(frame, (0,0), fx=resize, fy=resize))

        if count % 500 == 0:
            time_diff = frame_time - time_start
            fps = count / time_diff.total_seconds()
            print("FPS: " + str(fps))
            print("MMO:", shared_dict['motion_on'], shared_dict['motion_off'])
            count = 0 
            lc = lc + 1
            print ("LC:" + str(lc))
            time_start = frame_time
            log.write( frame_time.strftime("%Y%m%d%H%M%S") + "|FPS:" + str(fps) + "|\n")
            log.flush()
            cv2.imwrite("/var/www/html/out/latest.jpg", frames[0])

            file_exists = Path("/home/pi/fireball_camera/calnow");
            if (file_exists.is_file()):
                calnow = 1
            else:
                calnow = 0


        if lc < 3 or calnow == 1:
            shared_dict['motion_on'] = 0
            shared_dict['motion_off'] = 0 
            shared_dict['cnts'] = 0 
            #shared_dict['xywh'] = None
            #shared_dict['area'] = None 
            #shared_dict['perim'] = None 

  

      # check the lock, if it exists we need to dump the buffer
        #mmo= shared_dict['motion_on']; 
        #mmof= shared_dict['motion_off']; 
        #cnts= shared_dict['cnts']; 
        #if cnts > 0:
        #    (x,y,w,h) = shared_dict['xywh']; 
        #    area = shared_dict['area']; 
        #    perim = shared_dict['perim']; 
        #    avg_color = shared_dict['avg_color']; 
        #    middle_pixel = shared_dict['middel_pixel']; 
        #else: 
        #    (x,y,w,h) = (0,0,0,0) 
        #    shared_dict['area'] = 0
        #    shared_dict['xywh'] = None
        #    shared_dict['perim'] = 0
        #    shared_dict['avg_color'] = 0
        #    shared_dict['middle_pixel'] = 0

        #print("MMO:", shared_dict['cnts'], shared_dict['motion_on'], shared_dict['motion_off'], x,y,w,h,shared_dict['area'],shared_dict['perim'])
 
        #fds = str(shared_dict['cnts']) + "|" + str(shared_dict['motion_on']) + "|" + str(shared_dict['motion_off']) + "|" + str(x) + "|" + str(y) + "|" + str(w) + "|" + str(h) + "|" + str(shared_dict['area']) + "|" + str(shared_dict['perim']) + "|" + str(shared_dict['avg_color']) + "|" + str(shared_dict['middle_pixel'])
        fds = str(shared_dict['cnts']) + "|" + str(shared_dict['motion_on']) + "|" + str(shared_dict['motion_off']) + "|" 
        #frame_data.append(fds)

        if (shared_dict['motion_on'] >= 3 and shared_dict['motion_off'] >= 7 and lc > 4):
            #r = requests.get("http://" + config['cam_ip'] + "/webs/btnSettingEx?flag=1000&paramchannel=0&paramcmd=1058&paramctrl=25&paramstep=0&paramreserved=0&")

            #r = requests.get("http://" + config['cam_ip'] + "/webs/btnSettingEx?flag=1000&paramchannel=0&paramcmd=1058&paramctrl=50&paramstep=0&paramreserved=0&")
            print("RECORD BUFFER NOW!\n")
            shared_dict['motion_on'] = 0
            shared_dict['motion_off'] = 0 
            shared_dict['cnts'] = 0 
            mmo = 0
            mmof = 0
            lc = 0
            format_time = frame_time.strftime("%Y%m%d%H%M%S")
            outfile = "{}/{}.avi".format("/var/www/html/out", format_time)
            outfile_text = "{}/{}.txt".format("/var/www/html/out", format_time) 

            df = open(outfile_text, 'w', 1)
            dql = len(frame_times) - 2
            print (dql)
            time_diff = frame_times[1] - frame_times[dql]
            if time_diff.total_seconds() > 0:
                fps = 200 / time_diff.total_seconds()
            else: 
                fps = 20
            print ("FPS: ", fps)

            if int(config['hd']) == 0:
                frame_sz = cv2.resize(frames[0], (0,0), fx=1, fy=.75)
            else:
                frame_sz = frames[0]

            writer = cv2.VideoWriter(outfile, cv2.VideoWriter_fourcc(*'X264'), fps, (frame_sz.shape[1], frame_sz.shape[0]), True)
            while frames:
                img = frames.pop()
                img = cv2.resize(img, (0,0), fx=1, fy=.75)
                ft = frame_times.pop()
                #fd = frame_data.pop()
                format_time = ft.strftime("%Y-%m-%d %H:%M:%S.")
                dec_sec = ft.strftime("%f")
                format_time = format_time + dec_sec
                df.write(format_time + "|" + "|" + str(fps) + "|\n")
                writer.write(img)
                   #i = i + 1
            writer.release()
            df.close()
        count = count + 1

 
def show_loop(pipe_child, shared_dict):
    #cv2.namedWindow("pepe")
    config = read_config()


    print (config['cam_ip'])

    device_lat = config['device_lat']
    device_lng = config['device_lng']
    device_operator = config['first_name'] + " " + config['last_name']
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
    #frame_data = deque(maxlen=200)

    motion_on = 0
    motion_off = 0
    cnts = []
    lc = 1
    calibrate_now = 0
    calibrate_start = 0
    #sense_up = 0
 
    while True:
        frame = pipe_child.recv()
        alpha, tstamp_prev = iproc.getAlpha(tstamp_prev)
        #lock.acquire()
        #print ("SHOW LOOP:", count)

        #frame = cv2.resize(frame, (0,0), fx=0.8, fy=0.8)
        #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = cv2.GaussianBlur(frame, (21, 21), 0)
        if image_acc is None:
            image_acc = np.empty(np.shape(frame))
        image_diff = cv2.absdiff(image_acc.astype(frame.dtype), frame,)
        hello = cv2.accumulateWeighted(frame, image_acc, alpha)


        _, threshold = cv2.threshold(image_diff, 30, 255, cv2.THRESH_BINARY)
        thresh= cv2.dilate(threshold, None , iterations=2)
        (_, cnts, xx) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        #print(len(cnts), motion_on, motion_off)
        #print(cnts)
        if len(cnts) == 0:
            shared_dict['motion_off'] = shared_dict['motion_off'] + 1
            #middle_pixel = 0
            #avg_color = 0
        else:
            #area = cv2.contourArea(cnts[0])
            #perim = cv2.arcLength(cnts[0], True)
            #print ("Perim:", perim)
            #x,y,w,h = cv2.boundingRect(cnts[0])
            #x2 = x+w
            #y2 = y+h
            #mx = int(x + (w/2))
            #my = int(y + (h/2))
            #print ("XY:", x,x2,y,y2)
            #middle_pixel = frame[my,mx]
            #middle_sum = np.sum(middle_pixel)
            #crop_frame = frame[y:y2,x:x2]
            #avg_color_per_row = np.average(crop_frame, axis=0)
            #avg_color = np.average(avg_color_per_row, axis=0)



            #shared_dict['xywh'] = (x,y,w,h)
            #shared_dict['area'] = area
            #shared_dict['perim'] = perim
            #shared_dict['middel_pixel'] = middle_pixel 
            #shared_dict['avg_color'] = avg_color 

            shared_dict['motion_on'] = shared_dict['motion_on'] + 1
            shared_dict['motion_off'] = 0 
            shared_dict['cnts'] = len(cnts) 

            print("MMO:", shared_dict['cnts'], shared_dict['motion_on'], shared_dict['motion_off'])

        if shared_dict['motion_off'] > 5 and shared_dict['motion_on'] < 3:
            shared_dict['motion_on'] = 0
        #cv2.imshow('pepe', image_diff)
        #cv2.waitKey(5)
        count = count + 1

def write_buffer(frames):
    print ("YA, write")
    for i in range(len(frames), 0, -1):
         print (i)
         frames[i-0]



if __name__ == '__main__':
 
    print ("Capture Program")
    #logger = multiprocessing.log_to_stderr()
    #logger.setLevel(multiprocessing.SUBDEBUG)

    config = read_config()
    print (config['cam_ip'])
 
    os.system("./logger.py 'capture program started.'")

    try:
       if (config['device_lat'] != ''):
          print ("setup.")
    except:
          print ("device not setup yet.")
          exit()

 
    pipe_parent, pipe_child = multiprocessing.Pipe()
    man = multiprocessing.Manager()

    shared_dict = man.dict()
    shared_dict['motion_on'] = 0; 
    shared_dict['motion_off'] = 0; 


    cam_process = multiprocessing.Process(target=cam_loop,args=(pipe_parent, shared_dict))
    cam_process.start()
 
    show_process = multiprocessing.Process(target=show_loop,args=(pipe_child, shared_dict))
    show_process.start()

    cam_process.join()
    show_loop.join()
