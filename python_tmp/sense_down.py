#!/usr/bin/python3
import requests
from amscommon import read_config
config = read_config()
r = requests.get("http://" + config['cam_ip'] + "/webs/btnSettingEx?flag=1000&paramchannel=0&paramcmd=1058&paramctrl=50&paramstep=0&paramreserved=0&")

