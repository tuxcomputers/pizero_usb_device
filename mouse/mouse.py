#!/usr/bin/env python3
import time

def write_report(report):
        with open('/dev/hidg0', 'wb+') as fd:
            fd.write(report)

def alternate_left_right():
    s1 = b'\x00\xff\x00'
    s2 = b'\x00\x00\x00'

    write_report(s1)
    write_report(s2)

alternate_left_right()



