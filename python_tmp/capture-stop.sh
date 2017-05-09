#!/bin/bash

echo "Trying to stop capture...."
if `ps -aux | grep capture-hd.py |grep -v grep > /dev/null`;
then
     echo "Killing processes"
     echo  `ps -aux | grep capture-hd.py |grep -v grep| awk '{print $2}'`
     kill -9 `ps -aux | grep capture-hd.py |grep -v grep| awk '{print $2}'`
else
     echo "Already stopped."
fi

