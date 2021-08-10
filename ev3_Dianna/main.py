#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile, Font
import time
import socket

# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.


# Create your objects here.
ev3 = EV3Brick()


# Write your program here.
ev3.speaker.beep()
tiny_font = Font(size=18)
ev3.screen.set_font(tiny_font)



# Wait some time to look at the screen
'''
HOST = '127.0.0.1'
PORT = 2122
sk = socket.socket() # 默认使用IPV4和TCP
sk.bind((HOST,PORT))
sk.listen(1)

while True:
    cli, addr = sk.accept() # 等待连接(阻塞式),在连接到来之前会阻塞在这里
    data = cli.recv(1024).decode()
    ev3.screen.print('user-link')
    ev3.screen.print("data:",data)
    cli.send("FINISH".encode("utf-8"))
    ev3.screen.print("send:FINISH")
    cli.close()

'''