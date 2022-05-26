# !/usr/bin/env python3
# ## ###############################################
# file: yeelight.py
# file that simulate the API of yeelight
# Authors:
# Daniel Alberto Zarco Manzanares
# Octavio González Alcalá
# Carlos Colín Cosme
# Christian Otero García
# ## ###############################################
from time import sleep

import RPiVirtualBoard.RPi.GPIO as gpio


def servomotor_setting_angle(angle, pin):
    '''
    this function operate a servomotor with angle and pin for this purpse
    :param angle: angle for put into servomotor
    :param pin: pin where servomotor is connected
    :return:
    '''

    pos = float(angle)/10.+5.

    servo_pin = pin

    gpio.setmode(gpio.BOARD)
    gpio.setup(servo_pin, 100)
    frecuency_modulation = gpio.PWM(servo_pin, 50)
    frecuency_modulation.start(0)
    duty_cycle = angle / 20+2
    gpio.output(servo_pin, True)
    frecuency_modulation.ChangeDutyCycle(pos)
    sleep(1)
    gpio.output(servo_pin,False)
    frecuency_modulation.ChangeDutyCycle(0)
    frecuency_modulation.stop()
    gpio.cleanup()

def openDoor(pin):
    '''
    function to open door with 75º grades
    :param pin: pin where servomotor is connected
    :return:
    '''
    servomotor_setting_angle(75,pin)
    return

def closeDoor(pin):
    '''
    funtion to close door with 0º angle
    :param pin: pin where servomotor is connected
    :return:
    '''
    servomotor_setting_angle(0,pin)


