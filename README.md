[![N|Solid](http://www.amsmeteors.org/_members/ico/apple-touch-icon-114x114-precomposed.png)](http://www.amsmeteors.org)
# AMSCam

The AMSCam app allows you to interact with your AMS Cam & Raspberry Pi from a device on your network.

  - Browse detections
  - Setup / Config
  - Shutdown / Restart PI
  - ...
  
```diff
- WARNING: YOU NEED TO LAUNCH THIS APP BEFORE STARTING USING YOUR CAMERA
- AS IT IS REQUIRED TO UPDATE THE CAMERA PASSWORD FIRST.
```  
  



## Installation

### 1- Clone github repositories
Clone this repository and fireball_camera directory.

On your PI, go to /home/pi and:
```sh
$ cd /home/pi
$ git clone https://github.com/vperlerin/AMSCam.git
```

On your PI, /home/pi:
```sh
$ git clone https://github.com/mikehankey/fireball_camera.git
```

### Add your app as sudoer on the PI
On your PI, 
```sh
$ sudo vi /etc/sudoers

```
Then, add the following lines to the file:
```
www-data ALL=/sbin/shutdown
www-data ALL=NOPASSWD: /sbin/shutdown
www-data ALL=/sbin/restart
www-data ALL=NOPASSWD: /sbin/restart
```

## Add you as sudoer on the PI
```sh
$ sudo vi /etc/hosts
```
Then add the following line under root
```
127.0.1.1    ams[ID]
```
where [ID] is the ID of your Device (ex: ams22)

### Install 
On your PI, go to /home/pi/fireball_camera and:
```sh
$ sudo python ./setup/install.py
```

To see the app in action, open your browser (Firefox or Chrome) on your computer (warning: your computer has to be on the same LAN than the PI). Point your browser to 
```
http://[PI_IP]:80
```
> (replace [PI_IP] by the local IP of your Raspberry PI - ex: http://192.168.0.11:80/)

## Setup the autostart (optional)
If not already done, you can setup the automatic start of the AMSCam app on your PI:
```sh
$ sudo vi /etc/rc.local
```
Then, add the following line at the beginning of the file:
```
sudo /usr/local/bin/node /home/pi/AMSCam/app.js &
```
 

#  Troubleshooting

## Missing Python Packages

If you receive an error message about pycrypto / AES, please

```sh
$ sudo pip install pycrypto
```


## 'forever' Missing

If you receive an error message about forever, please

```sh
$ sudo npm install forever -g
```

## Stop the app from the PI
```sh
$ killall node
```
OR
```sh
$ killall forever
```

## Update Nodejs
You may want to update Nodejs on your Raspberry PI:
```sh
$ sudo npm cache clean -f
$ sudo npm install -g n
$ sudo n stable
$ sudo ln -sf /usr/local/n/versions/node/<VERSION>/bin/node /usr/bin/node 
```
ex: VERSION: 7.8.0

## Change VNC Viewer resolution
```sh
$ sudo raspi-config
> Advanced options
> Enable VNC Server
> Finish
```

```sh
$ sudo reboot
```

Once the PI has reboot:
```sh
$ sudo vi /boot/config.txt
```

And add the following lines:
```
hdmi_ignore_edid=0xa5000080
hdmi_group=2
hdmi_mode=85
```
Then, reboot the VNC Viewer. 
 
 
## Camera API Doc
See under /docs


## Log
* 2017/07/10 - Change port from 3000 to 80 (allow remote access)


## License

(The MIT License)

Copyright (C) 2011-2017 by Mike Hankey, LLC

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE
