[![N|Solid](http://www.amsmeteors.org/_members/ico/apple-touch-icon-114x114-precomposed.png)](http://www.amsmeteors.org)
# AMSCam

The AMSCam app allows you to interact with your AMS Cam & Raspberry Pi from a device on your network.

  - Browse detections
  - Setup / Config
  - Shutdown / Restart PI
  - ...

## Installation

### Clone this github repository
Clone this repository.
On your PI, go to /home/pi and:
```sh
$ cd /home/pi
$ git clone https://github.com/vperlerin/AMSCam.git
```

### Install Dependencies 
On your PI, go to /home/pi/AMSCam and:
```sh
$ sudo npm install 
$ sudo bower install
```
## Run the App
Under /home/pi/AMSCam, type
```sh
$ node app.js
```

To see the app in action, open your browser (Firefox or Chrome) on your computer (warning: your computer has to be on the same LAN than the PI). Point your browser to 
```
http://[PI_IP]:3000
```
> (replace [PI_IP] by the local IP of your Raspberry PI - ex: http://192.168.0.11:3000/)

## Setup the autostart
If not already done, you can setup the automatic start of the AMSCam app on your PI:
```sh
$ sudo vi /etc/rc.local
```
Then, add the following line at the beginning of the file:
```
sudo /usr/local/bin/node /home/pi/AMSCam/app.js &
```



#  Troubleshooting

## Add you as sudoer on the PI
```sh
$ sudo vi /etc/hosts
```
Then add the following line under root
```
127.0.1.1    ams[ID]
```
where [ID] is the ID of your Device (ex: ams22)

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
