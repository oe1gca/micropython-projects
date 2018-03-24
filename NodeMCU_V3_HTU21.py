# HTU21 I2C demo
# 2018/02/03 oe1gca	initial version for LoLin NodeMCU V3
# 

import utime
import math
from machine import Pin      
from machine import I2C 

def log10(x):
	y=math.log(x)* 0.43429
	return y

def read_htu_temp():
	i2c.writeto(64, b'\xf3')
	utime.sleep(0.055)
	data = i2c.readfrom(64,2)
	temp=data[0]*256+data[1]
	temp=-46.85 + 175.72 * temp / 65536.0
	return temp

def read_htu_rH():
	i2c.writeto(64, b'\xf5')
	utime.sleep(0.055)
	data = i2c.readfrom(64,2)
	rh=data[0]*256+data[1]
	rh=-6 + 125 * rh / 65536.0
	return rh

def read_htu_userreg():
	i2c.writeto(64, b'\xE7')
	utime.sleep(0.55)
	data = i2c.readfrom(64,1)
	return data[0]

def partial_pressure(t):
	A = 8.1332
	B = 1762.39
	C = 235.66
	pp = math.pow(10, A - B / (t + C))
	return pp

def dew_point_temp(rh, pp):
	A = 8.1332
	B = 1762.39
	C = 235.66
	td = -(B / (log10(rh * pp/100) - A) + C)
	return td
 
# initialize I2C 
# setup i2c bus on pins 4 & 5
i2c = I2C(scl=Pin(5), sda=Pin(4), freq=100000)

while True:
	print("HTU21 Temperature & rH Sensor Demo v1.0")
	print("User Register:         0x%02X" % read_htu_userreg())
	temp = read_htu_temp()
	rH = read_htu_rH()
	pp = partial_pressure(temp)
	print("Temperature:           %.2f C" % temp)
	print("Relative Humidity:     %.2f %%" % rH)
	print("Partial Pressure:      %.2f mmHg" % pp)
	print("Dew Point Temperature: %.2f C" % dew_point_temp(rH, pp))
	utime.sleep(10)
	print()


