# RaspberryPi Zero W as Virtual USB devices

This project was developed to turn a RaspberryPi Zero into different virtual USB devices

# Hardware requirements

1. [Raspberry Pi zero W](https://www.raspberrypi.org/products/raspberry-pi-zero-w/) x 1
1. Micro SD card x 1
1. [Raspberry Pi OS Lite](https://www.raspberrypi.org/software/operating-systems/#raspberry-pi-os-32-bit)


Notes:
1. You can use the original Zero and configure the USB port to act as a network adaptor but that is out of scope for this project
1. You can use one of the other OS packages if you wish and skip the install of the GPIO Python package install
1. Ensure you plug in the USB cable to the left hand side port, the right side is power only

# Software installation

Image the SD card with the image of the OS. There are many instructions on how to do this but my go to program is [balenaEtcher](https://www.balena.io/etcher/)

# Configure the Zero so it can act as a USB device

Enable libcomposite and other necessary modules and drivers
   ```
   sudo echo "dtoverlay=dwc2" | sudo tee -a /boot/config.txt
   sudo echo "dwc2" | sudo tee -a /etc/modules
   sudo echo "libcomposite" | sudo tee -a /etc/modules
   ```

# Follow the instructions inside one of the folders for the type of device you want to emulate
1. [Joystick](joystick)
1. [Mouse](mouse)