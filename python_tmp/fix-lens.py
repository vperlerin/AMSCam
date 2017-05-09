#lens_cal_file = "lens-cal.jpg"


import numpy as np
import cv2
import cv2 as cv
import glob
import os
cv2.namedWindow('pepe')
bad = []
good = []
# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((7*6,3), np.float32)
objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

images = glob.glob('jpgs/*.jpg')

x_points = []
y_points = []
count = 0
for fname in images:
    #print (fname)
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(gray, (7,6),None)
    #ret, corners = cv2.findCirclesGrid(gray, (6,3), flags = cv2.CALIB_CB_ASYMMETRIC_GRID + cv2.CALIB_CB_CLUSTERING)
    ret,corners= cv.findCirclesGrid(gray, (7,6))

    
    #for shit in corners:
    #   print shit




    # If found, add object points, image points (after refining them)
    if ret == True:
        objpoints.append(objp)

        cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
        imgpoints.append(corners)

        # Draw and display the corners
        cv2.drawChessboardCorners(img, (6,3), corners,ret)
        good.append(fname)

        mx = corners.max(axis=0)
        mn = corners.min(axis=0)

        x = mx[0][0]
        y = mx[0][1]
        x2 = mn[0][0]
        y2 = mn[0][1]
        x = int((x + x2) / 2)
        y = int((y + y2) / 2)
        cv2.circle(img, (x,y), 5, (255,0,0), thickness=1, lineType=8, shift=0) 
        #1280 / 720
        if x < 640:
           lr = "left"
        else: 
           lr = "right"
        if y > 360:
           ud = "down"
        else: 
           ud = "up"
        if x < 320:
           lr = "leftleft"
        if x > 980:
           lr = "rightright"
        if y < 250:
           ud = "upup"
        if y > 500:
           ud = "downdown"

        new_f = lr + ud + str(count) + ".jpg"
        cmd = "cp " + fname + " jpgs_sort/" + new_f
        print (cmd)
        os.system(cmd)
        print (fname, x,y, lr, ud)
        x_points.append(str(x) + "," + str(y))
        #y_points.append(x)
        ps = 0
        for point in x_points:
           tx,ty = point.split(",")
           cv2.circle(img, (int(tx),int(ty)), 5, (255,0,0), thickness=1, lineType=8, shift=0) 
           ps = ps + 1
           
        count = count + 1
    else:
        print ("Corners not found.", ret)
        bad.append(fname)
    #cv2.imshow('pepe',img)
    #cv2.waitKey(3)



exit()
#cv2.destroyAllWindows()
#ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None,None,None,flags=cv2.cv.CV_CALIB_FIX_ASPECT_RATIO)


ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None,None,None,flags=cv2.cv.CV_CALIB_USE_INTRINSIC_GUESS)

#print (ret, mtx, dist, rvecs, tvecs)
#print ("DIST: ", dist)

#dist = np.array([5.18,3.51,4.74,1.67,-2.44])

img = cv2.imread(fname)
#img = cv2.imread("jpgs/dump-0.jpg")
#img = cv2.imread('stars.jpg')
h, w = img.shape[:2]
newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))

# undistort
#print (dist)
dst = cv2.undistort(img, mtx, dist, None, newcameramtx)
#print ("MTX: ", mtx)
#print ("DIST: ", dist)
#print (dst)
#print (roi)
cv2.imshow('pepe',dst)
cv2.waitKey(0)
cv2.imwrite('calibresult.png',dst)


# crop the image
#x,y,w,h = roi
#print x,y,w,h
#dst = dst[y:y+h, x:x+w]
#cv2.imshow('pepe',dst)
#cv2.waitKey(0)

# undistort
mapx,mapy = cv2.initUndistortRectifyMap(mtx,dist,None,newcameramtx,(w,h),5)
dst = cv2.remap(img,mapx,mapy,cv2.INTER_LINEAR)
cv2.imshow('pepe',dst)
cv2.waitKey(0)

# crop the image
x,y,w,h = roi
#print (x,y,w,h)
#dst = dst[y:y+h, x:x+w]
#cv2.imshow('pepe',dst)
#cv2.waitKey(0)
cv2.imwrite('calibresult2.png',dst)

#print ("BAD FILES:")
for file in bad:
#   print (file)
   os.system("rm "+ file)
#print ("GOOD FILES:")
count = 0
for file in good:
   cmd = "mv " + file + " jpgs/temp-" + str(count) + ".jpg" 
   #print (cmd)
   #os.system(cmd)
   count = count + 1
count = 0
images = glob.glob('jpgs/*.jpg')
for file in images:
   #cmd = "mv " + file + " jpgs/rs-dump-" + str(count) + ".jpg" 
   #print (cmd)
   #os.system(cmd)
   count = count + 1

#print ("DIST: ", dist)
