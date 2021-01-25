from gpiozero import Button
from signal import pause
from time import sleep
from math import pow, floor

NULL_CHAR = chr(0)
xy_bytes_file      = open('/opt/joystick/joystick_xy_bytes', 'r')
xy_bytes           = int(xy_bytes_file.read())
button_bytes_file  = open('/opt/joystick/joystick_button_bytes', 'r')
button_bytes       = int(button_bytes_file.read())
report_length_file = open('/opt/joystick/report_length', 'r')
report_length      = int(report_length_file.read())

def clean_up():
    report = NULL_CHAR*report_length
    with open('/dev/hidg0', 'rb+') as fd:
        fd.write(report.encode())

def button(p):
    # The position of the data byte
    loc = int(floor(p-1)/8)
    
    # The required power is calculated
    power = p-(loc*8)-1
    
    # The character value is calculated
    x = int(pow(2, power))
    
    # First two bytes are for joystick XY, always 00
    # The number of padding bytes until the data is next
    # The data is added
    # The number of padding bytes to the end is added on the end, the 3 on the end of the formula is 2 x XY position bytes and the data byte
    #report = NULL_CHAR*2+NULL_CHAR*loc+chr(x)+NULL_CHAR*(report_length-loc-3)
    report = NULL_CHAR*xy_bytes+NULL_CHAR*loc+chr(x)+NULL_CHAR*(button_bytes-loc-1)
    
    with open('/dev/hidg0', 'rb+') as fd:
        fd.write(report.encode())
    
def js_button_1():
    button(1)

def js_button_10():
    button(10)

def js_button_18():
    button(18)

def js_button_26():
    button(26)

gpio_2 = Button(2)
gpio_2.when_pressed = js_button_1
gpio_2.when_released = clean_up

gpio_3 = Button(3)
gpio_3.when_pressed = js_button_10
gpio_3.when_released = clean_up

gpio_4 = Button(4)
gpio_4.when_pressed = js_button_18
gpio_4.when_released = clean_up

gpio_21 = Button(21)
gpio_21.when_pressed = js_button_26
gpio_21.when_released = clean_up


clean_up()
clean_up()
clean_up()

pause()
