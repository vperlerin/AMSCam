# DELETE DETECTIONS FILES
# with the following extensions: ".jpg","-objects.jpg","-summary.txt",".avi",".txt"

import os 
import sys
from os.path import isfile
import os.path
import re

#path print sys.argv[1] 
#file name  print sys.argv[2] 

extensions = [".jpg","-objects.jpg","-summary.txt",".avi",".txt"]
events = sys.argv[2].split(",")
toReturn = "" 
 
for event in events: 
    for ext in extensions: 
        f = sys.argv[1] + event + ext
        if os.path.isfile(f):
            os.remove(f)
            if ext in ['.txt']:
                m = re.search(r'(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})(\d{2})', event)
                if m:
                    event =  m.group(1)+'-'+m.group(2)+'-'+m.group(3)+' '+m.group(4)+':'+m.group(5)+':'+m.group(6)
            
                toReturn = toReturn + '$' + event
 
print toReturn