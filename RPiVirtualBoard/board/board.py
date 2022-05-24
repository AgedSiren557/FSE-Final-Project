#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# ## #############################################################
# board.py
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

import re
import sys
import time
# from queue import queue
from os import path, _exit
from threading import Thread
from tkinter import *

from PIL import Image, ImageTk, ImageEnhance

_img_path = path.join(path.dirname(path.realpath(__file__)), 'img')

def _img(file_name):
	return path.join(_img_path, file_name)

class LED:
	def __init__(self):
		self._on = False
		self._bg = PhotoImage(file=_img('led-background.png'))
		self._fg = PhotoImage(file=_img('led-foreground.png'))
		self._im = PhotoImage(file=_img('led-bright.png'))
	# end def


	def on(self):
		self._on = True
	# end def

	def off(self):
		self._on = False
	# end def

	def draw(self, canvas, xpos, ypos):
		canvas.create_image(xpos, ypos, anchor=NW, image=self._bg)
		if self._on:
			canvas.create_image(xpos, ypos, anchor=NW, image=self._im)
		canvas.create_image(xpos, ypos, anchor=NW, image=self._fg)
	# end def
#end class


class SevenSeg:
	def __init__(self):
		self._bgi = PhotoImage(file=_img('7s-background.png'))
		self._fgi = PhotoImage(file=_img('7s-foreground.png'))
		self._sai = PhotoImage(file=_img('7s-a.png'))
		self._sbi = PhotoImage(file=_img('7s-b.png'))
		self._sci = PhotoImage(file=_img('7s-c.png'))
		self._sdi = PhotoImage(file=_img('7s-d.png'))
		self._sei = PhotoImage(file=_img('7s-e.png'))
		self._sfi = PhotoImage(file=_img('7s-f.png'))
		self._sgi = PhotoImage(file=_img('7s-g.png'))
		self._dpi = PhotoImage(file=_img('7s-dp.png'))
		self.a = 0
		self.b = 0
		self.c = 0
		self.d = 0
		self.e = 0
		self.f = 0
		self.g = 0
		self.dp = 0
	# end def

	def draw(self, canvas, xpos, ypos):
		canvas.create_image(xpos, ypos, anchor=NW, image=self._bgi)
		if self.a:
			canvas.create_image(xpos, ypos, anchor=NW, image=self._sai)
		if self.b:
			canvas.create_image(xpos, ypos, anchor=NW, image=self._sbi)
		if self.c:
			canvas.create_image(xpos, ypos, anchor=NW, image=self._sci)
		if self.d:
			canvas.create_image(xpos, ypos, anchor=NW, image=self._sdi)
		if self.e:
			canvas.create_image(xpos, ypos, anchor=NW, image=self._sei)
		if self.f:
			canvas.create_image(xpos, ypos, anchor=NW, image=self._sfi)
		if self.g:
			canvas.create_image(xpos, ypos, anchor=NW, image=self._sgi)
		if self.dp:
			canvas.create_image(xpos, ypos, anchor=NW, image=self._dpi)
		canvas.create_image(xpos, ypos, anchor=NW, image=self._fgi)
	# end def

class BCD7Seg:
	def __init__(self, sevenSeg):
		self.sevenSeg = sevenSeg
		self._ena = 1
		self._bcd = 0
		self._rom = {
			#    0, 1, 2, 3, 4, 5, 6, 7, 8, 9, a, b, c, d, e, f
			0 : [1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1], # a
			1 : [1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0], # b
			2 : [1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0], # c
			3 : [1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0], # d
			4 : [1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1], # e
			5 : [1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1], # f
			6 : [0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1], # g
		}
	# end def

	@property
	def bcd(self):
		return self._bcd
	# end def

	@bcd.setter
	def bcd(self, value):
		if value < 0:
			value = 0
		if value > 15:
			value = 15
		self._bcd = value
		self.sevenSeg.a = self._rom[0][value] if not self._ena else 0
		self.sevenSeg.b = self._rom[1][value] if not self._ena else 0
		self.sevenSeg.c = self._rom[2][value] if not self._ena else 0
		self.sevenSeg.d = self._rom[3][value] if not self._ena else 0
		self.sevenSeg.e = self._rom[4][value] if not self._ena else 0
		self.sevenSeg.f = self._rom[5][value] if not self._ena else 0
		self.sevenSeg.g = self._rom[6][value] if not self._ena else 0
	# end def

	@property
	def ena(self):
		return self._ena
	# end def

	@ena.setter
	def ena(self, value):
		self._ena = value
		self.bcd = self._bcd
	# end def



class Board:
	def __init__(self):

		# GUI
		self.gui = Tk(className='GPIO LED Board')
		self.sevenSeg = SevenSeg()
		self.leds = [ LED() for i in range(0, 8) ]
		self.BCD7Seg = BCD7Seg(self.sevenSeg)
		self.BCD7Seg.ena = 0
		self._io_pins = {}
		for i in range(1, 28):
			self._io_pins[i] = None
		self._initialize_components()
		self.running = True
	# end def

	def __del__(self):
		_exit(1)

	def _initialize_components(self):
		# set window size
		self.gui.geometry("510x270")
		#set window color
		self.gui.configure(bg='#296e01')
		self.gui.protocol("WM_DELETE_WINDOW", self._on_closing)
		# Create canvas
		self.canvas = Canvas(self.gui, width=510, height=270, bg='#296e01', bd=0, highlightthickness=0, relief='ridge')
		self.canvas.pack()
		self._draw_canvas()
		self.canvas.after(1, self._redraw)
	# end def

	def _draw_canvas(self):
		self.canvas.delete(ALL)
		# Add 7-segments to canvas
		self.sevenSeg.draw(self.canvas, 197, 90)
		# Add LEDs to canvas
		xpos = 20
		ypos = 20
		for led in self.leds:
			led.draw(self.canvas, xpos, ypos)
			xpos += 60
		self.canvas.update()
	# end def

	def _redraw(self):
		self._update_status()
		self._draw_canvas()
		if self.running:
			self.canvas.after(20, self._redraw)
	# end def

	def _on_closing(self):
		self.running = False
		self.gui.destroy()
	# end def

	def _update_status(self):
		led_pins = [15, 18, 23, 24, 25, 8, 7, 12]

		# 16, 20, 21, 26
		if self._io_pins[16] and self._io_pins[20] and self._io_pins[21] and self._io_pins[26]:
			bcd = 8*self._io_pins[26].read()
			bcd+= 4*self._io_pins[21].read()
			bcd+= 2*self._io_pins[20].read()
			bcd+= 1*self._io_pins[16].read()
			self.BCD7Seg.bcd = bcd
		else:
			self.BCD7Seg.bcd = 0
		for i in range(len(led_pins)):
			if self._io_pins[led_pins[i]] and self._io_pins[led_pins[i]].read():
				self.leds[i].on()
			else:
				self.leds[i].off()
	# end def

	def connect(self, cable):
		"""cable is an dictionary of 27 objects with read() and write()
		methods whose keys are the number of the pin, starting in 1"""
		for pin in self._io_pins:
			if not pin in cable:
				continue
			if not hasattr(cable[pin], 'read'):
				raise Exception('{} object has no read attribute', cable[pin])
			self._io_pins[pin] = cable[pin]
		# end for
	# end def


