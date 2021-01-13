from gpiozero import Button
from signal import pause
from time import sleep
import math import pow

NULL_CHAR = chr(0)
sleep_time = 1
report_length = 6
def clean_up():
    report = NULL_CHAR*report_length
    with open('/dev/hidg0', 'rb+') as fd:
        fd.write(report.encode())

def button(p):
    if p <= 8:
        x = pow(2, p-1)
        report = chr(0)+chr(0)+chr(x)+chr(0)+chr(0)+chr(0)
    elif p <= 16:
        x = pow(2, p-9)
        report = chr(0)+chr(0)+chr(0)+chr(x)+chr(0)+chr(0)
    elif p <= 24:
        x = pow(2, p-17)
        report = chr(0)+chr(0)+chr(0)+chr(0)+chr(x)+chr(0)
    elif p <= 32:
        x = pow(2, p-25)
        report = chr(0)+chr(0)+chr(0)+chr(0)+chr(0)+chr(x)
    else:
        print ('Huh')
    with open('/dev/hidg0', 'rb+') as fd:
        fd.write(report.encode())
    sleep(sleep_time)
    clean_up()

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
gpio_3 = Button(3)
gpio_3.when_pressed = js_button_10
gpio_4 = Button(4)
gpio_4.when_pressed = js_button_18
gpio_21 = Button(21)
gpio_21.when_pressed = js_button_26



clean_up()
clean_up()
clean_up()

pause()
