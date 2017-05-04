import glob
import os
import json
import re
from os import listdir
from os.path import isfile, join
 
def read_file(file_path):
    config = ''
    file = open(file_path, "r")
    for line in file:
        config = config + line
    file.close()
    return(config)

data = {"detection":[]}
c = 0
for filename in glob.glob('/var/www/html/out/maybe/*.avi'):  
    filename = os.path.basename(filename)
    d = {}
    d['name']     = os.path.splitext(filename)[0]
    
    m = re.search(r'(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})(\d{2})', d['name'])
    
    if m:
         d['date'] =  m.group(1)+'-'+m.group(2)+'-'+m.group(3)+' '+m.group(4)+':'+m.group(5)+':'+m.group(6)
    
    d['video'] = d['name'] + ".avi"
    d['objects'] = d['name'] + "-objects.jpg"
    d['preview'] = d['name'] + ".jpg"
    d['summary'] = d['name'] + "-summary.txt"
    
    d['summaryTxt'] = read_file('/var/www/html/out/maybe/'+d['name'] + "-summary.txt")
    
    data["detection"].append({'detect': d})
    
print json.dumps(data)