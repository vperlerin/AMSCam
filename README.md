# AMS Cam

## Update Nodejs on PI
sudo npm cache clean -f
sudo npm install -g n
sudo n stable
sudo ln -sf /usr/local/n/versions/node/<VERSION>/bin/node /usr/bin/node 
#ex: VERSION: 7.8.0

## Copy all files on the PI
# (mkdir AMScam)
/home/pi/AMSCam

### Install Dependencies 
```
npm install 
bower install
```
### Start the server
```
node app.js
```
### Point your browser to `http://[PI_IP]:3000` and you should have the app running - ex: http://192.168.0.11:3000/
