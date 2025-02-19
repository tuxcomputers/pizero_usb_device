#!/bin/bash

do_log=1

cd ~/git/pizero_usb_device/mouse/

if [ $do_log = 1 ]; then
    now=`date +'%Y-%m-%d %H:%M:%S'`
    logName=`date +'%Y-%m-%d'`
    echo $now >> logs/$logName.log
fi

sudo python mouse.py

