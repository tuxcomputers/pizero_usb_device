# What I learnt while do ing this project

## HID descriptors
When HID devices connect they send across what length of data the computer should expect from the device. This is defined in the device creation script by this line:
```
echo 6 > functions/hid.usb0/report_length
```

Line 38 of joystick.sh contains the HID descriptors for the joystick, a decoding of that line looks like this:
```
0x05, 0x01,        // Usage Page (Generic Desktop Ctrls)
0x09, 0x04,        // Usage (Joystick)
0xA1, 0x01,        // Collection (Application)
0x15, 0x81,        //   Logical Minimum (-127)
0x25, 0x7F,        //   Logical Maximum (127)
0x09, 0x01,        //   Usage (Pointer)
0xA1, 0x00,        //   Collection (Physical)
0x09, 0x30,        //     Usage (X)
0x09, 0x31,        //     Usage (Y)
0x75, 0x08,        //     Report Size (8)
0x95, 0x02,        //     Report Count (2)
0x81, 0x02,        //     Input (Data,Var,Abs,No Wrap,Linear,Preferred State,No Null Position)
0xC0,              //   End Collection
0xA1, 0x00,        //   Collection (Physical)
0x05, 0x09,        //     Usage Page (Button)
0x19, 0x01,        //     Usage Minimum (0x01)
0x29, 0x20,        //     Usage Maximum (0x20)
0x15, 0x00,        //     Logical Minimum (0)
0x25, 0x01,        //     Logical Maximum (1)
0x75, 0x01,        //     Report Size (1)
0x95, 0x20,        //     Report Count (32)
0x81, 0x02,        //     Input (Data,Var,Abs,No Wrap,Linear,Preferred State,No Null Position)
0xC0,              //   End Collection
0xC0,              // End Collection

// 45 bytes
```

## Data packets
The data sent to the computer for the current configuration of the joystick contains 6 bytes, 2 are for the XY and 4 are the buttons. The first byte of the buttons data is for buttons 1 to 8, the next are for buttons 9-16.

If the bit is a 0 then the button is off, if it is a 1 then the button is on.

![Joystick device](/images/04-data.png)

## How the data packets are constructed
When the Zero wants to indicate that button 1 the bytes required are '001000', this third byte is converted to binary
00000001

When button 9 is required the bytes sent are 000100. It is the same byte but just in a different position, again the binary conversion is 00000001. However since it is in byte 4 the computer recognises that it is button 9 that is on.

This means that the only bytes required are, 1, 2, 4, 8, 16, 32, 64 and 128 (in Hex they are 01, 02, 04, 08, 10, 20, 40, 80). To use a different group of 8 buttons the same byte is used but it is in a different position.

To covert the button number to the required value 2 is raised to a power
Button 1 is 2^0 = 1
Button 2 is 2^1 = 2
Button 3 is 2^2 = 4
etc

## How the Python function uses the button number
When the function ```button(p)``` is called the button number desired is passed as the parameter ```p```

If the button number is less than 8 then power raised to is p-1, then the value is sent as the third byte.

Button 1 = 2^(1-1) = 2^0 = char(1)
Button 2 = 2^(2-1) = 2^1 = char(2)
Button 3 = 2^(3-1) = 2^2 = char(4)

If the button number is less than 16 the the power raised to is p-9, then that value is sent as the fourth byte.

Button 9 = 2^(9-9) = 2^0 = char(1)
Button 10 = 2^(11-9) = 2^1 = char(2)
Button 11 = 2^(12-9) = 2^2 = char(4)


## Altering the config to suit your own purposes
This config is for a joystick with XY plus 32 buttons, if you want more or less then you can do so by following these directions

### Altering the number of buttons
#### Decreasing the buttons to 16
Two alternatives, first is just leave it and use less than 32.

The second requires a couple of steps:
1. Reduce the number of bytes the computer is expecting
   - Line 35 of joystick.sh, 16 buttons only needs 4 bytes (2 for XY and 2 for the 16 buttons)
   - Line 38 of joystick.sh, change the max buttons and reported buttons to x10
1. Reduce the number of bytes sent to clear the button presses
   - Line 8 of the joystick.py
1. Remove the chr(0) not required from lines 17 and 20 of joystick.py

#### Increasing the number of buttons to 64
Why do this when the Zero only has 28 GPIO pins is baffling to me but it is possible.

1. Increase the number of bytes the computer is expecting to 10 (2 for XY, 8 for the buttons)
   - Line 35 of joystick.sh
1. Increase the number of bytes sent to clear the button presses
   - Line 8 of the joystick.py
1. Ensure every line sending bytes so it sends 10
1. Use the current function as a guide to increase the ```elif``` blocks

### Changing how the buttons operate
Currently the function to detect the GPIO change is 'when_pressed'
```gpio_2.when_pressed = js_button_1```

The ```button(p)``` function sends the bytes, waits for the amount of time set by the parameter ```sleep_time``` and then releases the button.

You can increase or reduce the amount of time the button is pressed.

Alternatively the call to ```clear_up``` could be removed from the button function and new lines added at the bottom for each button

```
gpio_2 = Button(2)
gpio_2.when_pressed = js_button_1
gpio_2.when_released = clear_up
```

Doing it like this would indicate the button is pressed while you have the finger on the button.