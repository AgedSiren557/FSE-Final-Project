#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# ## #############################################################
# GPIO.py
#
# Author: Mauricio Matamoros
# Licence: MIT
# Date:
#
# ## #############################################################
# Future imports (Python 2.7 compatibility)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from time import time, sleep
from threading import Thread
from random import seed, randint

# ## #############################################################
# Constants
# ## #############################################################
LOW = 0x00
HIGH = 0x01
BCM = 0x00
BOARD = 0x01
OUT = 0x01
IN = 0x00
# End constants




_io_mode = BCM
_pin_map = {
	#BOARD : BCM/GPIO
	 3 :  2,
	 5 :  3,
	 7 :  4,
	 8 : 14,
	10 : 15,
	11 : 17,
	12 : 18,
	13 : 27,
	15 : 22,
	16 : 23,
	18 : 24,
	19 : 10,
	21 :  9,
	22 : 25,
	23 : 11,
	24 :  8,
	26 :  7,
	27 :  0,
	28 :  1,
	29 :  5,
	31 :  6,
	32 : 12,
	33 : 13,
	35 : 19,
	36 : 16,
	37 : 26,
	38 : 20,
	40 : 21,
}

def _board2bcm(pin):
	return _pin_map.get(pin, -1)

def _check_pin(pin):
	if not isinstance(pin, int):
		raise ValueError("pin number must be an integer")
	if pin < 0 or pin > 27:
		raise ValueError("Not an I/O pin")

def setwarnings(flag):
	pass

def setmode(mode):
	global _io_mode
	_io_mode = mode

def setup(pin, io_mode, initial=LOW):
	if _io_mode == BOARD:
		pin = _board2bcm(pin)
	_check_pin(pin)
	_io_pins[pin].setup(io_mode, initial)

def input(pin):
	if _io_mode == BOARD:
		pin = _board2bcm(pin)
	_check_pin(pin)
	return _io_pins[pin].value

def output(pin, value):
	if _io_mode == BOARD:
		pin = _board2bcm(pin)
	_check_pin(pin)
	_io_pins[pin].value = value

def cleanup():
	for pwm in _pwms:
		pwm.stop()
		del pwm
	for pin in _io_pins:
		_io_pins[pin].setup(IN)

class PWM:
	def __init__(self, channel, frequency):
		_pwms.append(self)
		self._thread = None
		self._running = False
		self._duty_cycle = 0
		self._frequency = frequency

		if _io_mode == BOARD:
			channel = _board2bcm(channel)
		self._pin = _io_pins[channel]
	#end def

	def __del__(self):
		if self._thread is not None:
			self.stop()
		if _pwms is not None:
			for pwm in _pwms:
				if pwm is self:
					_pwms.remove(self)
					break
	#end def

	def _worker(self):
		self._running = True
		reset_time = 0
		flank_time = 0
		# run until stopped
		while self._running:
			now = int(time() * 1000)
			if now >= flank_time:
				self._pin.value = 0
			if now >= reset_time and self._frequency > 0:
				self._pin.value = 1
				reset_time = int(now + 1000.0 / self._frequency)
				flank_time = int(now + self._duty_cycle * 10.0 / self._frequency)
			sleep(0.001)
		#end while
	#end def

	def start(self, dc):
		self.ChangeDutyCycle(dc)
		self._thread = Thread(target=self._worker)
		self._thread.start()
	#end def

	def stop(self):
		if self._thread is not None:
			self._running = False
			if self._thread.is_alive():
				self._thread.join()
		self._thread = None
	#end def

	def ChangeFrequency(self, freq):
		if not isinstance(freq, int) and not isinstance(freq, float):
			raise TypeError("Invalid type")
		if freq < 0:
			raise ValueError("The frequency must be a positive number")
		elif freq == 0:
			self.stop()

		self._frequency = freq
	#end def

	def ChangeDutyCycle(self, dc):
		if dc < 0 or dc > 100:
			raise ValueError("dc out of range")
		self._duty_cycle = dc
	#end def
#end class

def _random_pin_value():
	return randint(0, 2)

class GPIO_PIN:
	def __init__(self, gpio_pin_num):
		self.gpio_pin_num = gpio_pin_num
		self._buffer = 0
		self.setup(IN)

	def setup(self, io_mode, initial_value=LOW):
		self.io_mode = io_mode
		if self.io_mode is OUT:
			self.value = initial_value

	@property
	def value(self):
			return self._buffer

	@value.setter
	def value(self, value):
		self.write(value)

	def _dump(self, value):
		pass

	def read(self):
		return self._buffer

	def write(self, value):
		if self.io_mode is OUT:
			self._buffer = 1 if value else 0

	def __repr__(self):
		if self.gpio_pin_num < 10:
			return 'GPIO 0{}'.format(self.gpio_pin_num)
		else:
			return 'GPIO {}'.format(self.gpio_pin_num)



seed(time())
_pwms = []
_io_pins = {}
for i in range(1, 28):
	_io_pins[i] = GPIO_PIN(i)
