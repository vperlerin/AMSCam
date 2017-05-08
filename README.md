# AMS Cam

This app allows you to interact with your AMS Cam & Raspberry Pi from a device on your network.

## Install


### Git Clone
Clone this directory to /home/pi  on your Raspberry Pi
```
git clone https://github.com/vperlerin/AMSCam.git
```

### Install Dependencies 
```
npm install 
bower install
```

### Start the server
Under /home/pi/AMSCam, type
```
node app.js
```

### Use your browser (Firefox or Chrome)
Point your browser to 
```
http://[PI_IP]:3000
```
(replace [PI_IP] by the local IP of your Raspberry PI - ex: http://192.168.0.11:3000/)


### Help
You may want to update Nodejs on your Raspberry PI:
```
sudo npm cache clean -f
sudo npm install -g n
sudo n stable
sudo ln -sf /usr/local/n/versions/node/<VERSION>/bin/node /usr/bin/node 
```
ex: VERSION: 7.8.0


### Changing the PI Resolution on the VNC Viewer
```
sudo raspi-config
> Advanced options
> Enable VNC Server
> Finish
```

```
sudo reboot
```

Once the PI has reboot:
```
sudo vi /boot/config.txt
```

And add the following lines:
```
hdmi_ignore_edid=0xa5000080
hdmi_group=2
hdmi_mode=85
```

Then, reboot the VNC Viewer. 


### Temporary
Please, add the .py files under python_tmp to the fireball_camera folder

