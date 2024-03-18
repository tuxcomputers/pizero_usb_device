#!/bin/bash

# Exit on first error.
set -e

# Echo commands before executing them, by default to stderr.
set -x

# Treat undefined environment variables as errors.
set -u

modprobe libcomposite

# mouse
cd /sys/kernel/config/usb_gadget/
mkdir -p isticktoit
cd isticktoit

# Define USB specification
echo 0x1d6b > idVendor # Linux Foundation
echo 0x0104 > idProduct # Multifunction Composite Gadget
echo 0x0100 > bcdDevice # v1.0.0
echo 0x0200 > bcdUSB # USB2

mkdir -p strings/0x409
echo "21011970" > strings/0x409/serialnumber
echo "Raynak Services" > strings/0x409/manufacturer
echo "Ultimate mouse" > strings/0x409/product
mkdir -p configs/c.1/strings/0x409
echo "Config 1: ECM network" > configs/c.1/strings/0x409/configuration
echo 250 > configs/c.1/MaxPower


# Add functions here
mkdir -p functions/hid.mouse
echo 0 > functions/hid.mouse/protocol
echo 0 > functions/hid.mouse/subclass
echo 7 > functions/hid.mouse/report_length
echo -ne echo -ne \\x05\\x01\\x09\\x02\\xA1\\x01\\x05\\x09\\x19\\x01\\x29\\x08\\x15\\x00\\x25\\x01\\x95\\x08\\x75\\x01\\x81\\x02\\x05\\x01\\x09\\x30\\x09\\x31\\x16\\x00\\x00\\x26\\xFF\\x7F\\x75\\x10\\x95\\x02\\x81\\x02\\x09\\x38\\x15\\x81\\x25\\x7F\\x75\\x08\\x95\\x01\\x81\\x06\\x05\\x0C\\x0A\\x38\\x02\\x15\\x81\\x25\\x7F\\x75\\x08\\x95\\x01\\x81\\x06\\xC0 > functions/hid.mouse/report_desc
ln -s functions/hid.mouse configs/c.1/

ls /sys/class/udc > UDC

chmod 777 /dev/hidg0

sleep 10
