import math
import sys
R = 6378.1



# usage
# python cams.py lat, lon, center_heading, el_start, fov_hdeg, fov_vdeg
# python cams.py 39.588747 -76.584339 34 10 70 60

def read_config():
    config = {}
    file = open("config.txt", "r")
    for line in file:
      line = line.strip('\n')
      data = line.rsplit("=",2)
      config[data[0]] = data[1]
      #print key, value
    return(config)



def find_point (lat, lon, d, brng):
   lat1 = math.radians(lat) #Current lat point converted to radians
   lon1 = math.radians(lon) #Current long point converted to radians

   lat2 = math.asin( math.sin(lat1)*math.cos(d/R) +
         math.cos(lat1)*math.sin(d/R)*math.cos(brng))

   lon2 = lon1 + math.atan2(math.sin(brng)*math.sin(d/R)*math.cos(lat1),
               math.cos(d/R)-math.sin(lat1)*math.sin(lat2))

   lat2 = math.degrees(lat2)
   lon2 = math.degrees(lon2)

   return(lat2, lon2)



def get_fov(device_lat, device_lng, center_heading, device_alt, heading, elv_angle):

    left_az = float(center_heading) - (float(cam_hdeg) / 2)
    if left_az < 0:
        left_az = left_az + 360
    right_az = float(center_heading) + (float(cam_hdeg) / 2)
    bottom_el = float(device_alt) - (float(cam_vdeg) / 2)
    bottom_el = float(device_alt) + (float(cam_vdeg) / 2) + 10
    ra = math.radians(20)
    dist_lb = 80/math.tan(ra)
    ra = math.radians(65)
    dist_lt = 80/math.tan(ra)

    print ("Dist:", dist_lb, dist_lt)

    device_lat = float(device_lat)
    device_lng = float(device_lng)


    (llc_lat, llc_lon) = find_point(device_lat, device_lng, dist_lb, math.radians(left_az))
    (ulc_lat, ulc_lon) = find_point(device_lat, device_lng, dist_lt, math.radians(left_az))
    (lrc_lat, lrc_lon) = find_point(device_lat, device_lng, dist_lb, math.radians(right_az))
    (urc_lat, urc_lon) = find_point(device_lat, device_lng, dist_lt, math.radians(right_az))

    cords = str(ulc_lon)+","+str(ulc_lat)+",80000\n" + str(urc_lon)+","+str(urc_lat)+",80000\n" + str(lrc_lon)+","+str(lrc_lat)+",80000\n" + str(llc_lon)+","+str(llc_lat)+",80000\n" + str(ulc_lon)+","+str(ulc_lat)+",80000\n"

    print ("<?xml version='1.0' encoding='UTF-8'?>")
    print ("<kml xmlns='http://www.opengis.net/kml/2.2'>")
    print ("<Document>")
    print ("<Style id='poly'>")
    print ("<PolyStyle>")
    print ("<color>550000cc</color>")
    print ("</PolyStyle>")
    print ("</Style>")
    print ("<Placemark>")
    print ("<styleUrl>#poly</styleUrl>")

    print("<Polygon>\n")
    print("<color>ff0000ff</color>\n")
    print("<extrude>0</extrude>\n")
    print("<altitudeMode>relativeToGround</altitudeMode>\n")
    print("<outerBoundaryIs>\n")
    print("<LinearRing>\n")
    print("<coordinates>\n")
    print (cords)
    print("</coordinates>\n")
    print("</LinearRing>\n")
    print("</outerBoundaryIs>\n")
    print("</Polygon>\n")
    print("</Placemark>\n")
    print("</Document>\n")
    print("</kml>\n")

    out = open("fov.txt", "w")
    out.write(cords)
    out.close

#    print ("ULC:", ulc_lat, ulc_lon)
#    print ("URC:", urc_lat, urc_lon)
#    print ("LLC:", llc_lat, llc_lon)
#    print ("LRC:", lrc_lat, lrc_lon)

#(x, device_lat, device_lng, center_heading, el_start, cam_hdeg, cam_vdeg) = sys.argv
config = read_config()
if len(sys.argv) > 1:
    config['heading'] = int(sys.argv[1])
get_fov(config['device_lat'], config['device_lng'], config['heading'], config['device_alt'], config['cam_fov_x'], config['cam_fov_y'])

