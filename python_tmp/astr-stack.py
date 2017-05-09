#!/usr/bin/python3 
#import collections
#from collections import deque
from PIL import Image, ImageChops
#from queue import Queue
#import multiprocessing
#import datetime
import cv2
import numpy as np
#import iproc 
import time
#import ephem
import sys
#import os

def view(file, show):

    out_file = file.replace(".avi", ".jpg")
    #print (file)
    #print (out_file)
    img_matrix = [] 
    count = 0
    print ("FILE:", file)
    cap = cv2.VideoCapture(file)
    time.sleep(2)
    frame = None 
    last_frame = None 
    image_acc = None 
    nc = 0
    while (frame is None):
        _ , frame = cap.read()
        print("Frame is none.")
        nc = nc + 1
        if nc > 20:
           print ("Can't read the file", file)
           exit()
    stack_frame = np.array(frame,dtype=np.float32)
    im = np.array(frame,dtype=np.float32)
    final_image = Image.fromarray(frame)
    #cv2.namedWindow('pepe')
    while True:
        _ , frame = cap.read()
        nice_frame = frame
        if frame is None:
            print (str(count) + " frames processed.")
            break
        else:
            frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
            frame_img = Image.fromarray(frame)
            final_image=ImageChops.lighter(final_image,frame_img)
            #im += np.array(frame_img, dtype=np.float32)

            alpha = .25
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame = cv2.GaussianBlur(frame, (21, 21), 0)
            if last_frame is None:
               last_frame = nice_frame
            if image_acc is None:
               image_acc = np.empty(np.shape(frame))
            image_diff = cv2.absdiff(image_acc.astype(frame.dtype), frame,)
            hello = cv2.accumulateWeighted(frame, image_acc, alpha)
            _, threshold = cv2.threshold(image_diff, 10, 255, cv2.THRESH_BINARY)
            thresh= cv2.dilate(threshold, None , iterations=2)
            (_, cnts, hierarchy) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if count < 20: 
               cnts is None
               hierarchy is None
            data = str(count) + "|"
            if len(cnts) > 0:
               hierarchy = hierarchy[0]
               for comp in zip(cnts,hierarchy):
                   cnt = comp[0]
                   ch = comp[1]
                   x,y,w,h = cv2.boundingRect(cnt)
                   cv2.rectangle(nice_frame,(x,y),(x+w,y+h),(0,255,0),2)

 
                   print (ch)
                   if ch[2] < 0:
                       print (ch[2])
                       cv2.drawContours(nice_frame, [cnt], 0, (255,0,255), 3)
                   elif ch[3] < 0:
                       cv2.drawContours(nice_frame, [cnt], 0, (0,255,0), 3)
               print (len(cnts), " contours found.", hierarchy[0])
               #cv2.imshow("pepe", nice_frame)
               #cv2.waitKey(1)



        count += 1  
    print (out_file)
    final_image.save(out_file, "JPEG")

    #im /= count  * .15

    #final_image = Image.fromarray(np.uint8(im.clip(0,255)))
    #final_image.save('all_averaged2.jpg', 'JPEG')

    #image_stack = np.dstack(tuple(img_matrix)) 
    #median_array = np.median(image_stack, axis=2)
    #cv2.imwrite("test.jpg", median_array)
    #med_out = Image.fromarray(np.uint8(median_array))
    #med_out.save('all_medout.jpg', 'JPEG')

view(sys.argv[1], "a")
