#!/bin/bash

echo "Trying to start capture...."

procount=$(ps -aux | grep capture-hd.py |grep -v grep| wc -l);
echo $procount
if [[ $procount -eq 3 ]]; then
     echo "Capture Processes Already Running. Start aborted."
elif [[ $procount -eq 2 ]]; then
     echo "Capture Processes Already Running. Start aborrted."
else
     echo "Capture Processes NOT Running. Starting...";
     sudo -H -u pi ./capture-hd.py &
fi
