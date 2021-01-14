from gpiozero import Button
from signal import pause
from time import sleep
from math import pow, floor

NULL_CHAR = chr(0)
report_length_file = open('/sys/kernel/config/usb_gadget/xac_joystick/functions/hid.usb0/report_length', 'r')
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
    report = NULL_CHAR*2+NULL_CHAR*loc+chr(x)+NULL_CHAR*(report_length-loc-3)
    
    with open('/dev/hidg0', 'rb+') as fd:
        fd.write(report.encode())
    
def js_button_1():
    button(1)

def js_button_2():
    button(2)

def js_button_3():
    button(3)

def js_button_4():
    button(4)

def js_button_5():
    button(5)

def js_button_6():
    button(6)

def js_button_7():
    button(7)

def js_button_8():
    button(8)

def js_button_9():
    button(9)

def js_button_10():
    button(10)

def js_button_11():
    button(11)

def js_button_12():
    button(12)

def js_button_13():
    button(13)

def js_button_14():
    button(14)

def js_button_15():
    button(15)

def js_button_16():
    button(16)

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
