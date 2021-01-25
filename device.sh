#!/bin/bash

# Create xac_joystick gadget
cd /sys/kernel/config/usb_gadget/
mkdir -p xac_joystick
cd xac_joystick

xy_bytes=2
button_bytes=4
total_bytes=$(( $xy_bytes + $button_bytes ))

mkdir -p /opt/joystick/
echo $xy_bytes > /opt/joystick/joystick_xy_bytes
echo $button_bytes > /opt/joystick/joystick_button_bytes
echo $total_bytes > /opt/joystick/report_length

# Define USB specification
echo 0x1d6b > idVendor  # Linux Foundation
echo 0x0104 > idProduct # Multifunction Composite Joystick Gadget
echo 0x0100 > bcdDevice # v1.0.0
echo 0x0200 > bcdUSB    # USB2
echo 0x02   > bDeviceClass
echo 0x00   > bDeviceSubClass
echo 0x00   > bDeviceProtocol

# Device information
mkdir -p strings/0x409
echo "21011970" > strings/0x409/serialnumber
echo "Hazza Industries" > strings/0x409/manufacturer
echo "RaspberryPi Joystick" > strings/0x409/product

# Create configuration file
mkdir -p configs/c.1/strings/0x409
echo 0x80 > configs/c.1/bmAttributes
echo 250  > configs/c.1/MaxPower # 250 mA
echo "Joystick configuration" > configs/c.1/strings/0x409/configuration

# Define the functions of the device
mkdir functions/hid.usb0
echo 0 > functions/hid.usb0/protocol
echo 0 > functions/hid.usb0/subclass
echo $total_bytes > functions/hid.usb0/report_length

# HID descriptor for a joystick with 32 buttons
echo -ne \\x05\\x01\\x09\\x04\\xA1\\x01\\x15\\x81\\x25\\x7F\\x09\\x01\\xA1\\x00\\x09\\x30\\x09\\x31\\x75\\x08\\x95\\x02\\x81\\x02\\xC0\\xA1\\x00\\x05\\x09\\x19\\x01\\x29\\x20\\x15\\x00\\x25\\x01\\x75\\x01\\x95\\x20\\x81\\x02\\xC0\\xC0 > functions/hid.usb0/report_desc
####                                                                                                                                                                        ^^ Max buttons                          ^^ Reported buttons

# Link the configuration file
ln -s functions/hid.usb0 configs/c.1

# Activate device 
sudo ls /sys/class/udc > UDC

sleep 10
