# RaspberryPi Zero W as a Virtual joystick
This project was developed to turn a RaspberryPi Zero into a virtual joystick

# Hardware requirements  

1. [Raspberry Pi zero W](https://www.raspberrypi.org/products/raspberry-pi-zero-w/) x 1
1. Micro SD card x 1
1. [Raspberry Pi OS Lite](https://www.raspberrypi.org/software/operating-systems/#raspberry-pi-os-32-bit)

Note: You can use the original Zero and configure the USB port to act as a network adaptor but that is out of scope for this project

Note2: You can use one of the other OS packages if you wish and skip the install of the GPIO Python package install

# Software installation
1. Image the SD card with the image of the OS. There are many instructions on how to do this but my go to program is [balenaEtcher](https://www.balena.io/etcher/)
1. Download the GPIO Python package:
     ```
     sudo apt-get update
     sudo apt-get -y install rpi.gpio python3-gpiozero
     ```

# Configure the Zero as a USB device
1. Enable libcomposite and other necessary modules and drivers
   ```
   sudo echo "dtoverlay=dwc2" | sudo tee -a /boot/config.txt
   sudo echo "dwc2" | sudo tee -a /etc/modules
   sudo echo "libcomposite" | sudo tee -a /etc/modules
   ```
1. Copy the USB device creation script to /usr/bin and make it executable
   ```
   sudo cp device.sh /usr/bin
   sudo chmod +x /usr/bin/device.sh
   ```
1. The RaspberryPi uses dynamic device creation so the creation script needs to be run every time the Pi boots. To configure the Zero to run the USB joystick device creation on boot add the following line above 'exit 0' to the file ```/etc/rc.local```
   ```
   /usr/bin/joystick.sh
   ```
1. Reboot the Zero
   ```
   sudo reboot
   ```
1. Connect the Zero to your computer, you should now see the virtual joystick in your devices
   - Control Panel -> Devices and Printers
   
   ![Joystick device](/images/01-device.png)

# Testing the virtual joystick
1. Right click the joystick and select
   ![Joystick device](/images/02-device.png)
   - Game controller settings
   - Properties button
   - Test tab
   
   ![Joystick device](/images/03-test.png)
1. On the Zero run the command:
   ```
   sudo python3 js_single_button.py
   ```
1. On the GPIO pins of the Zero connect the following pins to pin 6 (third from the top on the right) and this is the result you should see:
   1. Pin 3 (second left) - Button 1
   1. Pin 5 (third left)  - Button 10
   1. Pin 7 (fourth left) - Button 18
   1. Pin 40 (last right) - Button 26
1. To exit the script use Ctrl+C
1. Copy and paste the top 30+ lines of the test script to your own project
1. Configure the GPIO pins to trigger whichever joystick button you need

If you want to know all I have learned while creating this project so you can customise or change the configuration then read the 'About HID joysticks' file