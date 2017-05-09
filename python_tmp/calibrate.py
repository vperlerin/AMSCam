#!/usr/bin/python3 

import sys
import os
import subprocess

def do_it_all():
   # sense up and get deep exposure
   cmd = "./sense_up.py sense_up"
   output = subprocess.check_output(cmd, shell=True)
   print (output) 
   output = subprocess.check_output(cmd, shell=True)
   star_file = output.decode("utf-8")

   # stack the exposure 
   cmd = "./sense_up.py stack " + star_file 
   print (cmd) 
   output = subprocess.check_output(cmd, shell=True)
   output = output.decode("utf-8")
   print (output)


   # check to see if stars are present
   cal_file = star_file.replace(".avi", ".jpg")
   #cmd = "./count_stars.py " + cal_file
   #output = subprocess.check_output(cmd, shell=True)
   #output = output.decode("utf-8")
   #output = output.replace("\n", "") 
   #output = output.replace(" ", "") 
   #(trash, total_stars) = output.split(":")
   #print (total_stars)
   #if int(total_stars) > 0:
   #   print ("Plenty of stars. Try Plate Solve.") 
   #else:
   #   print ("Not enough stars. Calibration Failed.") 
   

   # plate solve the image 
   cmd = "./calibrate_image.py " + cal_file
   print (cmd) 
   output = subprocess.check_output(cmd, shell=True)
   output = output.decode("utf-8")
   print (output)

   # if plate solve succeeded, run the 4 corners
   wcs_file = cal_file.replace(".jpg", ".wcs")
   # check wcs_file
   cmd = "./4corners.py " + wcs_file
   print (cmd) 
   output = subprocess.check_output(cmd, shell=True)
   output = output.decode("utf-8")
   print (output)

   # now upload the calibration regardless of success or failure
   cmd = "./upload_calibration.py " + cal_file 
   print (cmd) 
   output = subprocess.check_output(cmd, shell=True)
   output = output.decode("utf-8")
   print (output)



if sys.argv[1] == 'all':
   print ("Do it all")
   do_it_all()
