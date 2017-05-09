
import os 
import glob
import time
from time import strftime
import datetime

def check_space():
 
    config = read_config();
    os.system("df -h " + config['output_dir'] + "> x")
    fp = open("x", "r")
    for line in fp:
        if "root" in line:
            line = line.replace("   ", " ")
            line = line.replace("  ", " ")
            el = line.split(" ")
            space_left = int(el[5].replace("%", ""))
            print ("Disk space at: " + str(space_left) + "%" )
    if space_left > 50:
        print ("Deleting files older than 21 days.")
        #files = glob.glob(config['output_dir'] + "/*.avi")
        path = config['output_dir']
        files = sorted(os.listdir(path), key=lambda f: os.path.getctime("{}/{}".format(path, f)))
        #print (files)
        total_files = len(files)
        three_weeks_ago = datetime.datetime.fromtimestamp(time.time() - 60 * 60 * 24 * 21)
        for file in files:
            fc = datetime.datetime.strptime(time.ctime(os.path.getctime("{}/{}".format(path, file))), "%a %b %d %H:%M:%S %Y")
            #fc = strftime("%a %b %d %H:%M%S %Y", time.ctime(os.path.getctime("{}/{}".format(path, file))))
            #fc = time.mktime(fc.timetuple())
            #print (fc, three_weeks_ago)
            if fc < three_weeks_ago:
                #print (file)
                cmd = "rm " + config['output_dir'] + "/" + file
                os.system(cmd)
                print (cmd)
    else:
        print ("File space ok, no files to delete.")


def read_config():
    config = {}
    file = open("config.txt", "r")
    for line in file:
      line = line.strip('\n')
      data = line.rsplit("=",2)
      config[data[0]] = data[1]
    return(config)


check_space()
