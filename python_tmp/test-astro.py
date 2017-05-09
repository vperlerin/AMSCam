import cv2
import numpy as np
import sys
import os


#os.system("/usr/bin/python /usr/local/astrometry/bin/text2fits.py -f \"ff\" -s \",\" /var/www/html/out/cal/20161222112409-stars-out.txt /var/www/html/out/cal/20161222112409-stars-out.fits")

#os.system("/usr/local/astrometry/bin/image2pnm.py --sanitized-fits-outfile sane.fits --fix-sdss --infile /var/www/html/out/cal/20161222112409-stars-out.fits --uncompressed-outfile uncomp --outfile out.pnm --ppm --verbose")


os.system("/usr/local/astrometry/bin/solve-field /var/www/html/out/cal/20161222112409.jpg --verbose --no-delete-temp --overwrite --width=640 --height=360 --width=640 --scale-low 50 --scale-high 95 ")
