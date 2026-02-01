# This is the instructions on how to configure the PiZero that you will connecting to the USB port

Run the following comnmands to install the module and run it
```
sudo apt-get install usbip
sudo modprobe usbip_host
```

Copy the file 'usbip.conf' to /etc/modules-load.d/
```
sudo cp usbip.conf /etc/modules-load.d/
```

Find the device using 'lsusb'

Copy the file 'usbipd.service' to /lib/systemd/system/

Edit file just copied, replace the XXXX:YYYY

Run the following commands to start the USB over IP service
```
sudo systemctl --system daemon-reload
sudo systemctl enable usbipd.service
sudo systemctl start usbipd.service
```