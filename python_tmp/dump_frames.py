import cv2
import sys
import glob
import time
config = {}
file = "chessboard.avi"
x_points = []
#cap = cv2.VideoCapture(file)
config['cam_ip'] = "192.168.1.91"
cap = cv2.VideoCapture("rtsp://" + config['cam_ip'] + "/av1_1&user=admin&password=admin")
list = glob.glob("jpgs/dump*")
count = len(list) - 1
if count < 0:
   count = 0
stop = count + 1300 
cv2.namedWindow("pepe")
#time.sleep(2)

while True:
   frame_file = "rs-dump-" + str(count) + ".jpg"
   _ , frame = cap.read()

   if frame is None:
      print ("NO FRAME!")
      exit()

   if count % 1 == 0:   
      gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)


      ret,corners= cv2.findCirclesGrid(gray, (6,3))

      if ret == True:
        cv2.drawChessboardCorners(gray, (6,3), corners,ret)

        #mx = corners.max(axis=0)
        #mn = corners.min(axis=0)

        #x = mx[0][0]
        #y = mx[0][1]
        #x2 = mn[0][0]
        #y2 = mn[0][1]
        #x = int((x + x2) / 2)
        #y = int((y + y2) / 2)
        #cv2.circle(gray, (x,y), 15, (255,0,0), thickness=5, lineType=8, shift=0)

        #ps = 0
        #for point in x_points:
        #   tx,ty = point.split(",")
        #   cv2.circle(gray, (int(tx),int(ty)), 15, (255,0,0), thickness=1, lineType=8, shift=0)
        #   ps = ps + 1


        cv2.imshow('pepe', gray)
        k = cv2.waitKey(0)
        if k == 27:
           exit()
 
        if k != 32:
           #x_points.append(str(x) + "," + str(y))
           cv2.imwrite("jpgs/" + frame_file, frame)
        if count > stop:
            print ("YO")
            #exit()
      else:
        print ("No board.")
        cv2.imshow('pepe', frame)
        k = cv2.waitKey(5)

   count = count + 1

