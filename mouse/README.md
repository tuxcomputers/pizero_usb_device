# RaspberryPi Zero W as a Virtual mouse

I developed this to use on my work laptop while I play games on my PS5. I cannot alter the time the screensaver takes to kick in.

While I am playing I have open on the laptop things such as maps and inventory managers.

When I needed to see or use those the screensaver had locked the laptop and I had to go through the annoying process to unlock it.

With this code the PiZero emulates a mouse and every 4 minutes sends a command to the laptop to move one pixel left and then one pixel right.

This is enough to stop the screensaver but not enough to notice if you are using the laptop at the time.

There are only 3 files involved:
1. activate_mouse.sh
1. mouse.py
1. mouse.sh

## activate_mouse.sh
This is the file that contains all of the code required on each boot up.

The USB system on the PiZero is dynamic and there is no persistant method to create the required entries

To make the PiZero start as a USB mouse on boot automatically you need to take the following steps

First add a symbolic link in the /usr/bin directory
```
cd /usr/bin
sudo ln -s ~/pizero_usb_device/mouse/activate_mouse.sh
```

Next add that to the rc.local to ensure it runs on every startup
```
cd /etc
sudo nano rc.local
```

Just above the 'exit' line add another line:
```
/usr/bin/activate_mouse.sh
```
1. Ctrl+X to exit the nano editor
1. respond Y when it asks if you want to save the file
1. hit enter to overwrite rc.local

Lastly ensure that the file is executable:
```
chmod u+x ~/pizero_usb_device/mouse/activate_mouse.sh
```
## mouse.py

This is the file that sends the information to the laptop to move one pixel left and then one pixel right.

There are two variables inside the alternate_left_right() function, s1 and s2, the middle packet of the stream are a signed hexidecimal numbers of 1 and -1

That function calls write_report with each variable in time. The write_report function opens the mouse device, writes the s1/s2 stream to it.

## mouse.sh

With the above two done the PiZero will automatically present itself as a mouse but it won't do anything. To make it useful and serve the purpose this script can be set to run every 4 minutes.

This file is a simple bash wrapper script that calls python to run the mouse.py file

If you do not want the date/time of when the script is called change the value of do_log to anything but a 1

All that is required now is to have the PiZero run this bash script, first open your crontab:
```
crontab -e
```
_If it asks which editor you want to use select nano_

Add a line to the file that the PiZero runs the script every 4 minutes:
```
*/4 * * * * ~/pizero_usb_device/mouse/mouse.sh
```
Close and save.

## Checking it works

Plug in your PiZero to your laptop, after a short time you should hear the usual sound of a new device being connected.

Check you have the "Ulitmate mouse" in your devices list

![Ultimate mouse](01-mouse.png)

If you wish to change the serial number, the manufacturer or the name of the mouse it can be done in the 'activate_mouse.sh' script lines 12 to 14