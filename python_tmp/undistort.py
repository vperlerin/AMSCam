import cv2
import sys
import numpy as np
file = sys.argv[1]
cv2.namedWindow('pepe')


camera_matrix = np.array([[1.64741907e+03,0.00000000e+00,6.28111780e+02], [0.00000000e+00,1.76942678e+03,3.63714363e+02], [0.00000000e+00,0.00000000e+00,1.00000000e+00]])

dist_coefs = np.array([[ -1.16938544,0.93515968,-0.04506055,0.02482632,2.01234356 ]])

img = cv2.imread(file)
h,  w = img.shape[:2]
newcameramtx, roi = cv2.getOptimalNewCameraMatrix(camera_matrix, dist_coefs, (w, h), 1, (w, h))
dst = cv2.undistort(img, camera_matrix, dist_coefs, None, newcameramtx)

outfile = file + '_undistorted.png'
print('Undistorted image written to: %s' % outfile)
cv2.imwrite(outfile, dst)
cv2.imshow('pepe', dst)
cv2.waitKey(0)



