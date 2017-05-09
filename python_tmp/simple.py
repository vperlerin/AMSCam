from collections import deque
from queue import Queue
import multiprocessing
import datetime
import cv2
import numpy as np
import iproc 
import time
MORPH_KERNEL = np.ones((10, 10), np.uint8)
record = 0
 
def cam_loop(pipe_parent):
   # cap = cv2.VideoCapture(0)
    cap = cv2.VideoCapture("rtsp://192.168.1.88/av0_1&user=admin&password=admin")

    #cap.set(3, 720.0)
    #cap.set(4, 480.0)
    #cap.set(3, 640.0)
    #cap.set(4, 480.0)
    #cap.set(3, 360.0)
    #cap.set(3, 320.0)
    #cap.set(4, 240.0)
    #cap.set(3, 480.0)
    #cap.set(4, 360.0)
 
    while True:
        _ , frame = cap.read()
        if frame is not None:
            pipe_parent.send(frame)
 
def show_loop(pipe_child):
    image_acc = None
    cal_image = None
    nice_image_acc = None
    stack = None
    tstamp_prev = None
    cv2.namedWindow('pepe')
    count = 0
    time_start = datetime.datetime.now()
    Q = None
    frame = pipe_child.recv()
    #frames = deque(np.empty(np.shape(frame)), maxlen=256)
    frames = deque(maxlen=256)
    firstFrame = None
    motion_on = 0
    motion_off = 0

    while True:
        frame = pipe_child.recv()
        frames.appendleft(frame)
        if firstFrame is None:
            firstFrame = frame 
            stack = frame 
            continue

        if count % 1 == 0: 
            nice_frame = frame
            alpha, tstamp_prev = iproc.getAlpha(tstamp_prev)
            if nice_image_acc is None:
                nice_image_acc = np.empty(np.shape(frame))
            nice_image_diff = cv2.absdiff(nice_image_acc.astype(frame.dtype), nice_frame,)
            hello = cv2.accumulateWeighted(nice_frame, nice_image_acc, alpha)
            #hellp = cv2.addWeighted(nice_image_acc,.5, nice_frame, .5, .5 )
            stack = stack + frame
            if count % 30 == 0:
               stack = frame
            nice_avg = cv2.convertScaleAbs(nice_image_acc)

            frame = cv2.resize(frame, (0,0), fx=0.5, fy=0.5)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame = cv2.GaussianBlur(frame, (21, 21), 0)
            if image_acc is None:
                image_acc = np.empty(np.shape(frame))
            image_diff = cv2.absdiff(image_acc.astype(frame.dtype), frame,)
            hello = cv2.accumulateWeighted(frame, image_acc, alpha)

            if cal_image is None:
               cal_image = nice_image_acc

            if count % 30 == 0:
               cal_image = cal_image + nice_image_acc

            cal_image_show = cv2.convertScaleAbs(cal_image)

            if count % 100 == 0: 
               cal_iamge = nice_image_acc

            #avg = cv2.convertScaleAbs(image_acc)
            _, threshold = cv2.threshold(image_diff, 30, 255, cv2.THRESH_BINARY)
            thresh= cv2.dilate(threshold, None , iterations=2)
            (_, cnts, xx) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if len(cnts) == 0:
               motion_off = motion_off + 1
            else:
               motion_on = motion_on + 1
               motion_off = 0

            #for c in cnts:
            ##   if cv2.contourArea(c) < 100:
            #       continue
            #   motion_on = motion_on + 1
            #   motion_off = 0
            if motion_off > 10 and motion_on < 10:
               motion_on = 0
               motion_off = 0

            if motion_off > 20 and motion_on > 10:
               print ("RECORD BUFFER NOW!")
               motion_off = 0
               motion_on = 0
               #write_buffer(frames)
               i = 1000 
               timestamp = datetime.datetime.now()
               outfile = "{}/{}.avi".format("out",
               timestamp.strftime("%Y%m%d-%H%M%S"))
               if record == 1: 
                   writer = cv2.VideoWriter(outfile, cv2.VideoWriter_fourcc(*'MJPG'), 25, (frames[0].shape[1], frames[0].shape[0]), True)
                   while frames:
                       img = frames.pop()

                       #cv2.putText(img, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S.%f%p"),
                       #(10, img.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1)
                       #cv2.imwrite("out/" + str(i) + ".jpg", img)
                       writer.write(img)
                       i = i + 1
                   writer.release()

            print ("motion_on, motion off, contours", motion_on, motion_off, len(cnts))
            #(x, y, w, h) = cv2.boundingRect(c)
            #cv2.rectangle(frame, (x, y), (x + w, y + w), (0, 255, 0), 2)

            #closed = cv2.morphologyEx(dilated, cv2.MORPH_CLOSE, MORPH_KERNEL)
            cv2.imshow('pepe', nice_frame)
            #cv2.imshow('pepe', cal_image_show)
            #cv2.imshow('pepe', cv2.convertScaleAbs(image_diff))
            cv2.waitKey(1)

        count = count + 1

        now = datetime.datetime.now()
        delta = now - time_start 
        limit = delta.total_seconds()
        #if limit < 13 and limit >= 2: 
        #    print ("LIMIT:", limit)
            #cv2.imwrite("out/" + str(count) + ".jpg", frame)
        #else:
            #exit()
        
 
def write_buffer(frames):
    print ("YA, write")
    for i in range(len(frames), 0, -1):
         print (i)
         frames[i-0]



if __name__ == '__main__':
 
    logger = multiprocessing.log_to_stderr()
    logger.setLevel(multiprocessing.SUBDEBUG)
 
    pipe_parent, pipe_child = multiprocessing.Pipe()
 
    cam_process = multiprocessing.Process(target=cam_loop,args=(pipe_parent, ))
    cam_process.start()
 
    show_process = multiprocessing.Process(target=show_loop,args=(pipe_child, ))
    show_process.start()

    cam_process.join()
    show_loop.join()
