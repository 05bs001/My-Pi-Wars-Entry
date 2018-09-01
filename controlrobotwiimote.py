import cwiid
from cwiid import *
import math
from serial import Serial
from time import sleep
from gpiozero import CamJamKitRobot

# define robot
robot = CamJamKitRobot()

# define method to try to connect to wiimote recursively
def connectToWiimote():
    print("Press 1+2 on your Wiimote now...")
    wm = None
    while not wm:
        try:
            wm = cwiid.Wiimote()
        except RuntimeError:
            print("Connection failed, trying again")
    print("connected to wiimote")
    wm.led = 1 # turn on 1st led on wiimote
    return wm

# define method to get wiimote joystick position
def getjoystickposition(wiimote):
    return wiimote.state['nunchuk']['stick']

# define method to scale wiimote joystick position to standard coordinates
def scale(x, y, oldminx, oldminy, oldmaxx, oldmaxy, newminx, newminy, newmaxx, newmaxy):
    # scale y
    yolddiff = oldmaxy - oldminy
    ynewdiff = newmaxy - newminy
    newy = (((y - oldminy) * ynewdiff) / yolddiff) + newminy
    
    # scale x
    xolddiff = oldmaxx - oldminx
    xnewdiff = newmaxx - newminx
    newx = (((x - oldminx) * xnewdiff) / xolddiff) + newminx
    
    return newx, newy

# define method to mix joystick signal to tank drive
def steering(x, y): # input -100 to 100, output same
    if abs(x) <= 10: x = 0 # avoid accidental movements
    if abs(y) <= 10: y = 0
    # main conversion
    x = -x
    v = (100-abs(x)) * (y/100) + y
    w = (100-abs(y)) * (x/100) + x
    r = (v + w) / 2
    l = (v - w) / 2
    return l, r

# connect wiimote
wiimote = connectToWiimote()

# tell wiimote to report data back
wiimote.rpt_mode = RPT_STATUS | RPT_BTN | RPT_ACC | RPT_IR | RPT_NUNCHUK | RPT_CLASSIC | RPT_BALANCE | RPT_MOTIONPLUS | RPT_EXT | MESG_STATUS | MESG_BTN | MESG_ACC | MESG_IR | MESG_NUNCHUK
wiimote.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_ACC | cwiid.RPT_EXT

# wait for wiimote to detect nunchuk
print('waiting for nunchuk to be detected')
while not 'nunchuk' in wiimote.state: pass
print('nunchuk detected')
print('starting main loop')

# main loop
while True:
    # get joystick position
    joystickpos = getjoystickposition(wiimote)
    # scale joystick position to standard coordinates
    joystickpos = list(scale(joystickpos[0], joystickpos[1], 23, 36, 227, 227, 0, 0, 200, 200))
    joystickpos[0] -= 100
    joystickpos[1] -= 100
    # get motor speeds based on joystick position
    motorspeeds = list(steering(joystickpos[0], joystickpos[1]))
    motorspeeds[0] /= 100
    motorspeeds[1] /= 100
    #print('motor speeds {0}'.format(motorspeeds))
    
    # send motor speeds to motor controller
    robot.value = motorspeeds[::-1]
