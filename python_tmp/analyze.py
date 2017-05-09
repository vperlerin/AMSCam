from collections import deque
from PIL import Image, ImageChops
from queue import Queue
import multiprocessing
import datetime
import cv2
import numpy as np
import iproc
import time
import sys
MORPH_KERNEL       = np.ones((10, 10), np.uint8)
count = 0
event = sys.argv[1]
event.replace(".
file = "/var/www/html/out/" + sys.argv[1]
tstamp_prev = None
image_acc = None
m_image_acc = None
cap = cv2.VideoCapture(file)
cv2.namedWindow('pepe')

open("jpgs/" + event + ".txt")
while True:
    _ , frame = cap.read()
    if (_ is True):
        print ("Count: ", count)

        alpha, tstamp_prev = iproc.getAlpha(tstamp_prev)
        if image_acc is None:
            image_acc = np.empty(np.shape(frame))
        image_diff = cv2.absdiff(image_acc.astype(frame.dtype), frame,)
        hello = cv2.accumulateWeighted(frame, image_acc, alpha)

        mframe = frame
        mframe = cv2.cvtColor(mframe, cv2.COLOR_BGR2GRAY)
        mframe = cv2.GaussianBlur(mframe, (21, 21), 0)
        if m_image_acc is None:
            m_image_acc = np.empty(np.shape(mframe))
        m_image_diff = cv2.absdiff(m_image_acc.astype(mframe.dtype), mframe,)
        hello = cv2.accumulateWeighted(mframe, m_image_acc, alpha)

        sframe = cv2.convertScaleAbs(image_acc)
        cv2.imshow('pepe', sframe)
        cv2.waitKey(1) 
        if count == 0:
            im = np.array(frame,dtype=np.float32)
        else:
            im += np.array(frame, dtype=np.float32)
        count = count + 1
    else:
        im /= count * 0.5
        final_image = Image.fromarray(np.uint8(im.clip(0,255)))
        final_image.save('all_averaged.jpg', 'JPEG')
        cv2.imshow('pepe', final_image)
        time.sleep(2)
        exit() 
