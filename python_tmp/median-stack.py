#!/usr/bin/python3 
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

def view(file, show):
    img_matrix = [] 
    count = 0
    cap = cv2.VideoCapture(file)
    while True:
        _ , frame = cap.read()
        img_matrix.append(gray_frame)
        if frame is None:
            print (str(count) + " frames processed.")
            break
        count += 1  

    image_stack = np.dstack(tuple(img_matrix)) 
    median_array = np.median(image_stack, axis=2)
    cv2.imwrite("test.jpg", median_array)

view("/var/www/html/out/" + sys.argv[1], "a")
