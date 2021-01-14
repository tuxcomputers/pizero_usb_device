# What I learnt while doing this project

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

When button 9 is required the bytes sent are 000100. It is the same data byte but just in a different position, again the binary conversion is 00000001. However since it is in byte 4 the computer recognises that it is button 9 that is on.

This means that the only bytes required are, 1, 2, 4, 8, 16, 32, 64 and 128 (in Hex they are 01, 02, 04, 08, 10, 20, 40, 80). To use a different group of 8 buttons the same byte is used but it is in a different position.

## How the Python function uses the button number
When the function ```button(p)``` is called the button number desired is passed as the parameter ```p```

To convert the button number requires several steps
1. The position number of the data byte, buttons 1-8 will have a position number of 0, 9-16 a position number of 1, etc (see above diagram)
   ```
   loc = int(floor(p-1)/8)
   ```
1. Next the power number is calculated using the position number
   ```
   power = p-(loc*8)-1
   ```
1. The data byte is calculated
   ```
   x = int(pow(2, power))
   ```
   - For example when the button is 9 the calculation for the power variable is:
   9-(1*8)-1 this equals 0, when 2 is raised to the power of zero it equals 1, so the data byte in binary is 00000001
   - When the button is 15 the calculation is:
   15-(1*8)-1 this equals 1, when 2 is raised to the power of 6 it equals 64, in binary that is 01000000
1. The data bytes are composed consisting of:
   - Two NULLS for the XY joystick position
   - The ```loc``` variable is used to add the padding between the Xy and the data
   - The data byte
   - The padding added to the end is
     - the ```report_length``` minus
     - the 2 XY position bytes minus
     - the data byte minus
     - the front button padding bytes

## Altering the config to suit your own purposes
This config is for a joystick with XY plus 32 buttons, if you want more or less then you can do so by following these directions

### Altering the number of buttons

If you require less buttons then just use less buttons. Why anyone would configure the Zero to have more than 32 when it only has 28 GPIO pins is baffling to me. However if you truly wish to alter the number of buttons it is possible.

1. Edit ```joystick.sh```
   1. Alter the length of the data packet the computer is expecting on this line, the value is number of buttons divided by 8 plus the two XY bytes:
      ```
      echo 6 > functions/hid.usb0/report_length
      ```
      - 3 is 8 buttons
      - 4 is 16 buttons
      - 5 is 24 buttons
      - etc
   1. On the HID descriptor line change the max and expected number of buttons
1. Edit the Python script, change the ```report_length``` to match the above


### Changing how the buttons operate
The Zero detects when a GPIO pin is set connected to ground (0v) and calls a function
```
gpio_2 = Button(2)
gpio_2.when_pressed = js_button_1
```

That function then calls the ```button(p)``` function with the button number as the parameter:
```
def js_button_1():
    button(1)
```

It is not possible to call the button function directly on the button press:
```
gpio_2.when_pressed = button(1)
```

That library just doesn't work that way, not my fault, sorry.

On detection of the release the data sent to the computer is all zeros by calling the ```clear_up``` function

This configuration only allows the pressing of a single button at a time.

It is possible to send data that indicates that multiple buttons are on at once for example the data '001100' would be button 1 and 9 are on.

If I required that the functionality for my project the button function would be WAY more complex. I would probably end up using some sort of data array to store the state of the buttons, convert that to hex and send that as the data. On GPIO state change I would then update the array convert it and send the data again, something like that anyway.