# This is the instruction on how to connect the machine to the USB over IP host

The USB host needs to be setup and configured first, the XXXX:YYYY is needed to connect tot he USB host

Run the commands
```
apt-get install linux-tools-generic
modprobe vhci-hcd
```

Copy the file 'usbip.conf' to /etc/modules-load.d/

Copy the file 'usbip.service' to /lib/systemd/system/
Edit file just copied, replace the XXXX:YYYY

```
sudo systemctl --system daemon-reload
sudo systemctl enable usbip.service
sudo systemctl start usbip.service
```

