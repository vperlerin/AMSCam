#!/usr/bin/python3
import os
import subprocess
import sys
import ephem
import math
from amscommon import read_config
from amscommon import write_config 
from amscommon import put_device_info 
R = 6378.1

def Decdeg2DMS( Decin ):
   Decin = float(Decin)
   if(Decin<0):
      sign = -1
      dec  = -Decin
   else:
      sign = 1
      dec  = Decin

   d = int( dec )
   dec -= d
   dec *= 100.
   m = int( dec*3./5. )
   dec -= m*5./3.
   s = dec*180./5.

   if(sign == -1):
      out = '-%02d:%02d:%06.3f'%(d,m,s)
   else: out = '+%02d:%02d:%06.3f'%(d,m,s)

   return out
   

def RAdeg2HMS( RAin ):
   RAin = float(RAin)
   if(RAin<0):
      sign = -1
      ra   = -RAin
   else:
      sign = 1
      ra   = RAin

   h = int( ra/15. )
   ra -= h*15.
   m = int( ra*4.)
   ra -= m/4.
   s = ra*240.

   if(sign == -1):
      out = '-%02d:%02d:%06.3f'%(h,m,s)
   else: out = '+%02d:%02d:%06.3f'%(h,m,s)
   
   return out

def find_corner (file, x, y):
   cmd = "/usr/local/astrometry/bin/wcs-xy2rd -w " + file + " -x " + x + " -y " + y 
   output = subprocess.check_output(cmd, shell=True)
   (t, radec) = output.decode("utf-8").split("RA,Dec")
   radec = radec.replace('(', '')
   radec = radec.replace(')', '')
   radec = radec.replace('\n', '')
   radec = radec.replace(' ', '')
   ra, dec = radec.split(",")
   print ("ASTR RA/DEC: ", ra,dec)
   radd = float(ra)
   decdd = float(dec)
   ra= RAdeg2HMS(ra)
   #(h,m,s) = ra.split(":")
   #ra = h + " h " + m + " min"
   dec = Decdeg2DMS(dec)
   return(ra, dec, radd, decdd)

def radec_to_azel(ra,dec,lat,lon,alt, caldate):
   body = ephem.FixedBody()
   print ("BODY: ", ra, dec)
   body._ra = ra
   body._dec = dec
   #body._epoch=ephem.J2000 

   obs = ephem.Observer()
   obs.lat = ephem.degrees(lat)
   obs.lon = ephem.degrees(lon)
   obs.date = caldate 
   print ("CALDATE:", caldate)
   obs.elevation=float(alt)
   body.compute(obs)
   az = str(body.az)
   el = str(body.alt)
   (d,m,s) = az.split(":")
   dd = float(d) + float(m)/60 + float(s)/(60*60)
   az = dd

   (d,m,s) = el.split(":")
   dd = float(d) + float(m)/60 + float(s)/(60*60)
   el = dd
   #az = ephem.degrees(body.az)
   return(az,el)

def find_point (lat, lon, d, brng):
   print ("Bearing is ", brng)
   lat1 = math.radians(lat) #Current lat point converted to radians
   lon1 = math.radians(lon) #Current long point converted to radians

   lat2 = math.asin( math.sin(lat1)*math.cos(d/R) +
         math.cos(lat1)*math.sin(d/R)*math.cos(brng))

   lon2 = lon1 + math.atan2(math.sin(brng)*math.sin(d/R)*math.cos(lat1),
               math.cos(d/R)-math.sin(lat1)*math.sin(lat2))

   lat2 = math.degrees(lat2)
   lon2 = math.degrees(lon2)

   return(lat2, lon2)


config = read_config()


if 1 == 1:
   

   el = sys.argv[1].split("/")
   caldate = el[-1] 
   file = sys.argv[1]
   #caldate = sys.argv[1]
   y = caldate[0:4]
   m = caldate[4:6]
   d = caldate[6:8]

   #t = caldate[8:14]
   h = caldate[8:10]
   mm = caldate[10:12]
   s = caldate[12:14]
   caldate = y + "/" + m + "/" + d + " " + h + ":" + mm + ":" + s 
   print (caldate)
   cords = ""

    #'center_ra_dec' : '90.00|90.00',
    #'center_az_el' : '90.00|90.00',
    #'center_az_el' : '90.00|90.00',
    #'pixel_scale' : 2.123,
    #'ulc_ra_dec' : '90.00|90.00',
    #'urc_ra_dec' : '90.00|90.00',
    #'llc_ra_dec' : '90.00|90.00',
    #'lrc_ra_dec' : '90.00|90.00',
    #'ulc_az_el' : '90.00|90.00',
    #'urc_az_el' : '90.00|90.00',
    #'llc_az_el' : '90.00|90.00',
    #'lrc_az_el' : '90.00|90.00',

   # Upper Left
   (ra, dec, radd, decdd) = find_corner(file, "1", "1")
  
   print ("RA/DEC of 1,1:", ra,dec)
   (az, el) = radec_to_azel(ra,dec,config['device_lat'],config['device_lng'],config['device_alt'], caldate)
   print ("RA/DEC of 1,1:", ra,dec)
   print ("AZ/EL of 1,1:", az,el)
   if el < 10:
      el = 10
   
   dist = 80/math.tan(math.radians(el))
   p1, p2 = find_point(float(config['device_lat']), float(config['device_lng']), dist, math.radians(az))
   print ("{0} km Distance to 80km altitude at {1} elevation angle for top left corner.".format( dist, el))
   print (p1,p2)
   cords_start = "{0:.2f}".format(p2) + "," + "{0:.2f}".format(p1) + ",0\n"
   cords = "{0:.2f}".format(p2) + "," + "{0:.2f}".format(p1) + ",0\n"
   print ("")
   config['ulc_ra_dec'] = "{0:.2f}".format(radd) + "|{0:.2f}".format(decdd)
   config['ulc_az_el'] = "{0:.2f}".format(az) + "|{0:.2f}".format(el)


   # Upper Right 
   (ra, dec, radd, decdd) = find_corner(file, "640", "1")
   print ("RA/DEC of 640,1:", ra,dec)
   (az, el) = radec_to_azel(ra,dec,config['device_lat'],config['device_lng'],config['device_alt'], caldate)
   print ("AZ/EL of 640,1:", az,el)
   if el < 10:
      el = 10
   dist = 80/math.tan(math.radians(el))
   p1, p2 = find_point(float(config['device_lat']), float(config['device_lng']), dist, math.radians(az))
   cords = cords + "{0:.2f}".format(p2) + "," + "{0:.2f}".format(p1) + ",0\n"
   print ("{0} km Distance to 80km altitude at {1} elevation angle for top right corner.".format( dist, el))
   print ("")
   config['urc_ra_dec'] = "{0:.2f}".format(radd) + "|{0:.2f}".format(decdd)
   config['urc_az_el'] = "{0:.2f}".format(az) + "|{0:.2f}".format(el)



   # Lower Right 
   (ra, dec, radd, decdd) = find_corner(file, "640", "380")
   print ("RA/DEC of 640,380:", ra,dec)
   (az, el) = radec_to_azel(ra,dec,config['device_lat'],config['device_lng'],config['device_alt'], caldate)
   print ("AZ/EL of 640,380:", az,el)
   if el < 10:
      el = 10
   dist = 80/math.tan(math.radians(el))
   p1, p2 = find_point(float(config['device_lat']), float(config['device_lng']), dist, math.radians(az))
   cords = cords + "{0:.2f}".format(p2) + "," + "{0:.2f}".format(p1) + ",0\n"
   print ("{0} km Distance to 80km altitude at {1} elevation angle for bottom right corner.".format( dist, el))
   print ("")
   config['lrc_ra_dec'] = "{0:.2f}".format(radd) + "|{0:.2f}".format(decdd)
   config['lrc_az_el'] = "{0:.2f}".format(az) + "|{0:.2f}".format(el)

   # Lower Left 
   (ra, dec, radd, decdd) = find_corner(file, "1", "380")
   print ("RA/DEC of 1,380:", ra,dec)
   (az, el) = radec_to_azel(ra,dec,config['device_lat'],config['device_lng'],config['device_alt'], caldate)
   print ("AZ/EL of 1,380:", az,el)
   if el < 10:
      el = 10
   dist = 80/math.tan(math.radians(el))
   p1, p2 = find_point(float(config['device_lat']), float(config['device_lng']), dist, math.radians(az))
   cords = cords + "{0:.2f}".format(p2) + "," + "{0:.2f}".format(p1) + ",0\n"
   print ("{0} km Distance to 80km altitude at {1} elevation angle for bottom left corner.".format( dist, el))
   print ("")
   config['llc_ra_dec'] = "{0:.2f}".format(radd) + "|{0:.2f}".format(decdd)
   config['llc_az_el'] = "{0:.2f}".format(az) + "|{0:.2f}".format(el)

   (ra, dec, radd, decdd) = find_corner(file, "320", "190")
   print ("CENTER RA/DEC of 320,190:", ra,dec)
   (az, el) = radec_to_azel(ra,dec,config['device_lat'],config['device_lng'],config['device_alt'], caldate)
   print ("AZ/EL of 320,190:", az,el)
   config['heading'] = str(az)
   config['elv_angle'] = str(el)
   config['center_ra_dec'] = "{0:.2f}".format(radd) + "|{0:.2f}".format(decdd)
   config['center_az_el'] = "{0:.2f}".format(az) + "|{0:.2f}".format(el)

   cmd = "/usr/local/astrometry/bin/wcsinfo " + file + " | grep pixscale" 
   output = subprocess.check_output(cmd, shell=True)
   print (output)
   (t, pixel_scale) = output.decode("utf-8").split(" ")
   pixel_scale = pixel_scale.replace("\n", "")
   config['pixel_scale'] = pixel_scale
   
   config['fov'] = cords.replace("\n", "|")
   write_config(config)
   put_device_info(config)



   cords = cords + cords_start
 
   kml = "<?xml version='1.0' encoding='UTF-8'?>"
   kml = kml + "<kml xmlns='http://www.opengis.net/kml/2.2'>"
   kml = kml + "<Document>"
   kml = kml + "<Style id='poly'>"
   kml = kml + "<PolyStyle>"
   kml = kml + "<color>550000cc</color>"
   kml = kml + "</PolyStyle>"
   kml = kml + "</Style>"
   kml = kml + "<Placemark>"
   kml = kml + "<styleUrl>#poly</styleUrl>"

   kml = kml + "<Polygon>\n"
   kml = kml + "<color>ff0000ff</color>\n"
   kml = kml + "<extrude>0</extrude>\n"
   kml = kml + "<altitudeMode>clampedToGround</altitudeMode>\n"
   kml = kml + "<outerBoundaryIs>\n"
   kml = kml + "<LinearRing>\n"
   kml = kml + "<coordinates>\n"
   kml = kml + cords
   kml = kml + "</coordinates>\n"
   kml = kml + "</LinearRing>\n"
   kml = kml + "</outerBoundaryIs>\n"
   kml = kml + "</Polygon>\n"
   kml = kml + "</Placemark>\n"
   kml = kml + "</Document>\n"
   kml = kml + "</kml>\n"

   fp = open("kml.kml", "w")
   fp.write(kml)
   fp.close()
   fp = open("fov.txt", "w")
   fp.write(cords)
   fp.close()
