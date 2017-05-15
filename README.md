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
sudo npm install 
sudo bower install
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

### Auto start App.js on reboot
Open /etc/rc.local
```
sudo vi /etc/rc.local
```
Then, add the following line at the beginning of the file:
```
sudo /usr/local/bin/node /home/pi/AMSCam/app.js &
```

### Add you as sudoer on the PI
```
sudo vi /etc/hosts
```
Then add the following line under root
```
127.0.1.1    ams[ID]
```
where [ID] is the ID of your Device (ex: ams22)


### Autostart the App on the PI
```
sudo vi /etc/rc.local

```
Then add the following lines to the file:
```
cd /home/pi/AMSCam/
forever start app.js &
exit 0

```
Reboot the PI if necessary.


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

