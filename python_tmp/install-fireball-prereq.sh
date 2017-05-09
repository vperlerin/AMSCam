#sudo mkdir /var/www
#sudo mkdir /var/www/html
#sudo mkdir /var/www/html/out
#sudo mkdir /var/www/html/out/false
#sudo mkdir /var/www/html/out/maybe
#sudo mkdir /var/www/html/out/cal
#sudo chown -R pi:pi /var/www
#exit()


## enable shell login on pi
## enable vnc login on pi raspi-config
## sudo apt-get --yes --force-yes update
## sudo apt-get --yes --force-yes dist-upgrade
## sudo apt-get --yes --force-yes upgrade
#
## install opencv per this doc
## http://www.pyimagesearch.com/2016/04/18/install-guide-raspberry-pi-3-raspbian-jessie-opencv-3/
#
##sudo apt-get --yes --force-yes install build-essential cmake pkg-config
#sudo apt-get --yes --force-yes install libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev
#sudo apt-get --yes --force-yes install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
#sudo apt-get --yes --force-yes install libxvidcore-dev libx264-dev
#sudo apt-get --yes --force-yes install libgtk2.0-dev
#sudo apt-get --yes --force-yes install libatlas-base-dev gfortran
#sudo apt-get --yes --force-yes install python2.7-dev python3-dev
#cd ~
#wget -O opencv.zip https://github.com/Itseez/opencv/archive/3.1.0.zip
#unzip opencv.zip
#wget -O opencv_contrib.zip https://github.com/Itseez/opencv_contrib/archive/3.1.0.zip
#unzip opencv_contrib.zip

#sudo apt-get install -y tesseract-ocr libtesseract-dev libleptonica-dev

#
##python
#wget https://bootstrap.pypa.io/get-pip.py
#sudo python3 get-pip.py
#pip install numpy
#pip install netifaces
#sudo pip install pyephem

#sudo apt-get install python3-dateutil
#sudo apt-get install python3-pil
#sudo pip install pytesseract

#
##compile opencv
#


cd ~/opencv-3.1.0/
#mkdir build
cd build
#make clean
cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D INSTALL_PYTHON_EXAMPLES=ON \
    -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib-3.1.0/modules \
    -D WITH_OPENMP=ON \
    -D BUILD_EXAMPLES=ON ..
make -j4
# if errors then compile on 1 core
sudo make install
sudo ldconfig

# NEED TO INSTALL GCC6 FOR ASTROMETRY TO WORK
#awk '{gsub(/\jessie/,"stretch"); print}' /etc/apt/sources.list > sources.list.x
#sudo cp sources.list.x /etc/apt/sources.list
#sudo apt-get update
#sudo apt-get install gcc-6 g++-6
#awk '{gsub(/\stretch/,"jessie"); print}' /etc/apt/sources.list > sources.list.x
#sudo cp sources.list.x /etc/apt/sources.list
#sudo apt-get update
#sudo apt --fix-broken install

# INSTALL ASTROMETRY.NET PRE-REQUISITS
#sudo apt-get install libwcs4
#sudo apt-get install wcslib-dev

# Set gcc6 as CC env var 
#CC=/usr/bin/gcc-6
#export CC

#NETPBM_INC=-I/usr/include
#NETPBM_LIB=/usr/lib/libnetpbm.a
#export NETPBM_INC
#export NETPBM_LIB

#WCS_SLIB="-Lwcs"
#WCSLIB_INC="-I/usr/local/include/wcslib-5.15"
#WCL_LIB="-Lwcs"
#export WCS_SLIB
#export WCSLIB_INC
#export WCS_LIB

#sudo apt-get --yes --force-yes install libcairo2-dev libnetpbm10-dev netpbm \
#                       libpng12-dev libjpeg-dev python-numpy \
#                       python-pyfits python-dev zlib1g-dev \
#                       libbz2-dev swig libcfitsio-dev
#wget http://astrometry.net/downloads/astrometry.net-latest.tar.gz
#gunzip astrometry.net-latest.tar.gz
#tar xf astrometry.net-latest.tar

#sudo mv /usr/bin/gcc /usr/bin/gcc.bak
#sudo ln -s /usr/bin/arm-linux-gnueabihf-gcc-6 /usr/bin/gcc

#cd astrometry.net-*
#sudo make
#sudo make py
#sudo make extra
#sudo make install

#when done
#sudo rm /usr/bin/gcc
#sudo mv /usr/bin/gcc.back /usr/bin/gcc
#index-4116.fits  index-4117.fits  index-4118.fits  index-4119.fits

#wget http://broiler.astrometry.net/~dstn/4100/index-4116.fits
#sudo mv index-4116.fits /usr/local/astrometry/data 
#wget http://broiler.astrometry.net/~dstn/4100/index-4117.fits
#sudo mv index-4117.fits /usr/local/astrometry/data 
#wget http://broiler.astrometry.net/~dstn/4100/index-4118.fits
#sudo mv index-4118.fits /usr/local/astrometry/data 
#wget http://broiler.astrometry.net/~dstn/4100/index-4119.fits
#sudo mv index-4119.fits /usr/local/astrometry/data 
