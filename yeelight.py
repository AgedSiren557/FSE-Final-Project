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

class Bulb:
    '''
    class that simulate the class bulb of yeelight
    '''
    def __init__(self, ip=127.0.0.1):
        '''
        this constructor create a object Bulb with an ip
        :param ip: the ip of the bulb 
        :return:
        '''
        self.ip = ip

    def turn_on(self):
        '''
        this method simulate the action of turning on the light
        :return:
        '''
        print("Turning on light\n")

    def turn_off(self):
        '''
        this method simulate the action of turning off the light
        :return:
        '''
        print("Turning off light\n")

    def set_brightness(self, val):
        '''
        this method simulate the action of setting the brightness of the light
        :param val: value of the brightness the bulb will take
        :return:
        '''
        print(f'Setting light to {val} \n')

    