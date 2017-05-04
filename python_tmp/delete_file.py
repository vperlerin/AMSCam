import os 
import sys
from os.path import isfile
import os.path

#path print sys.argv[1] 
#file name  print sys.argv[2] 

extensions = [".jpg","-objects.jpg","-summary.txt",".avi",".txt"]
 
for ext in extensions: 
    f = sys.argv[1] +sys.argv[2]+ext
    if os.path.isfile(f):
        os.remove(f)
 
print sys.argv[2]; 