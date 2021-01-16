from gpiozero import Button
from signal import pause
from time import sleep
from math import pow, floor
import subprocess

# list of bits, representing the 32 buttons
binaryList = [0] * 32
# Report hex values, will be populated at a later date
hexList = [None] * 4
NULL_CHAR = chr(0)
report_length_file = open('/sys/kernel/config/usb_gadget/xac_joystick/functions/hid.usb0/report_length', 'r')
report_length      = int(report_length_file.read())

# image display maybe
# image = subprocess.Popen('feh --hide-pointer -x -q -B black -g 1280x800 /home/pi/images/eliteD.png'.split())

def clean_up():
    report = NULL_CHAR*report_length
    with open('/dev/hidg0', 'rb+') as fd:
        fd.write(report.encode())

def sendReport():
    report = NULL_CHAR*2+''.join(hexList)

    with open('/dev/hidg0', 'rb+') as fd:
        fd.write(report.encode())
def compileReport():
    print('compilereport')
    # go through the bytes we want to send. 4 because we have 32 buttons
    for x in range(len(hexList)):
        # initialise some stuff
        hexList[x] = None
        bitsReverseString = ''

        # get the bits
        bitsReverse = binaryList[x*8:(x*8)+8]
        # and then WE REVERSE THEM because they are backwards in the byte
        # without this, button 2 would be triggered by GPIO 7, and 1 by 8, etc.
        bitsReverse.reverse()

        for y in range(len(bitsReverse)):
            bitsReverseString += str(bitsReverse[y])

        hexList[x] = hex(int(bitsReverseString,2))
def modifyBit(button, val='flip'):
    print('modbit')
    # button 1 is bit 0 so we -1 to turn the button number into the list position\
    pos = button - 1

    # check if its been changed to something valid
    if (val != 'flip') and (val==1 or val==2):
        # turn our button into the value
        binaryList[pos] = val
    else:
        # its just been flipped so we change it
        if (binaryList[pos] == 1):
            binaryList[pos] = 0
        else:
            binaryList[pos] = 1
def button(butt, val='flip'):
    print('button action '+str(butt)+' '+str(val))
    modifyBit(butt, val)
    compileReport()
    sendReport()

def activate(butt):
    button(butt, 1)
    print('activate')
def deactivate(butt):
    print('deactivate')
    button(butt, 0)

def screen():
    image = subprocess.Popen('feh --hide-pointer -x -q -B black -g 256x160 images/atreides.png'.split())
# def button(p):
#     # The position of the data byte
#     loc = int(floor(p-1)/8)

#     # The required power is calculated
#     power = p-(loc*8)-1

#     # The character value is calculated
#     x = int(pow(2, power))

#     # First two bytes are for joystick XY, always 00
#     # The number of padding bytes until the data is next
#     # The data is added
#     # The number of padding bytes to the end is added on the end, the 3 on the end of the formula is 2 x XY position bytes and the data byte
#     report = NULL_CHAR*2+NULL_CHAR*loc+chr(x)+NULL_CHAR*(report_length-loc-3)

#     with open('/dev/hidg0', 'rb+') as fd:
#         fd.write(report.encode())

def activate1():
    activate(1)
    print('act1')
def deactivate1():
    deactivate(1)
    print('deact1')

def activate2():
    activate(2)
    print('act2')
def deactivate2():
    deactivate(2)
    print('deact2')

def activate3():
    activate(3)
    print('act3')
def deactivate3():
    deactivate(3)
    print('deact3')

def activate4():
    activate(4)
    print('act4')
def deactivate4():
    print('deact4')
    deactivate(4)

# Using GPIO 0 to 15
print('startgpios')
gpio_0 = Button(0)
gpio_0.when_pressed = activate1
gpio_0.when_released = deactivate1

gpio_1 = Button(1)
gpio_1.when_pressed = activate2
gpio_1.when_released = deactivate2

gpio_2 = Button(2)
gpio_2.when_pressed = activate3
gpio_2.when_released = deactivate3

gpio_3 = Button(3)
gpio_3.when_pressed = activate4
gpio_3.when_released = deactivate4

gpio_4 = Button(4)
gpio_4.when_pressed = screen

print('stopgpios')
# Gpio 16 to 19 will be for internal changes

clean_up()
clean_up()
clean_up()

pause()
