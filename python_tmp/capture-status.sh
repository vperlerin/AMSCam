#!/bin/bash


procount=$(ps -aux | grep capture-hd.py |grep -v grep| wc -l);
echo $procount
if [[ $procount -eq 6 ]]; then
     echo "Capture Processes Running"
elif [[ $procount -eq 5 ]]; then
     echo "Capture Processes Running..."
else
     echo "Capture Processes NOT Running. Starting...";
     /home/pi/fireball_camera/capture-stop.sh
     sleep 5
     /home/pi/fireball_camera/capture-start.sh
fi

echo "check defunct"
defunct=$(ps -aux | grep capture-hd.py |grep defunct| wc -l);
echo $defunct
if [[ $defunct -eq 1 ]]; then
     echo "Capture Processes Defunct. Restarting..."
     /home/pi/fireball_camera/capture-stop.sh
     sleep 5
     /home/pi/fireball_camera/capture-start.sh
fi

