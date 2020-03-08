import os
import sys
import time
import select
import termios
import tty
from math import fmod, sqrt
from random import randint
class jet():
	def __init__(self,x,y):
		self.__x=x
		self.__y=y
		self.__vx=0
		self.__vy=0
		self.__fx = 0
		self.__lifes = 10
	def get_life(self):
		return self.__lifes
	
	def set_life(self,value):
		self.__lifes = value
    
	def get_x(self):
		return self.__x
	def set_x(self,value):
		self.__x = value
	def get_y(self):
		return self.__y
	def set_y(self,value):
		self.__y = value

	def get_vx(self):
		return self.__vx
	def set_vx(self,value):
		self.__vx = value
	def get_vy(self):
		return self.__vy
	def set_vy(self,value):
		self.__vy = value
	
	def moveup(self):
		self.__vy -= 0.3
	def moveleft(self):
		self.__vx -= 0.2
	def moveright(self):
		self.__vx += 0.2	
	def gravity(self):
		self.__vy+=0.1
	def update(self):
		self.__x+=self.__vx
		self.__y+=self.__vy
		xc = self.__x
		yc = self.__y
		if xc <=1:
			self.__x=2
			self.__vy=0
			self.__vx=0
		if xc >150:
			self.__x=150
			self.__vy=0
			self.__vx=0
		if yc <= 7:
			self.__y=7
			self.__vy=0
			self.__vx=0
		if yc > 35:
			self.__y=35
			self.__vx=0
			self.__vy=0

	def printp(self):
		xc=int(self.__x)
		yc=int(self.__y)
		print("\033[{};{}H <~@~>".format(yc,xc))




