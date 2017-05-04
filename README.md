# AMS Cam

This app allows you to interact with your AMS Cam & Raspberry Pi from a device on your network.

## Install


### Git Clone
Clone this directory to /home/pi/AMSCam on your Raspberry Pi


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