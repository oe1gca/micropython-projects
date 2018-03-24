# Wmos D1 mini with memsic C2120M compass sensor
# distribute data via Thingspeak
# Channel ID: <channel id>
# Field 1: Compass value
# Field 2: field_x
# Field 3: field_y
#
# oe1gca, March 2018

from machine import Pin,I2C
from utime import sleep
from math import atan2
from math import pi
import network
import ussl as ssl
import usocket as _socket
import ussl as ssl

led=Pin(2,Pin.OUT)
led.value(1)
i2c=I2C(scl=Pin(5), sda=Pin(4))

API_KEY = "<our write api key"
HOST = "api.thingspeak.com"

def set_coil():
	i2c.writeto(0x30, b'\x00\x02')
	sleep(0.001)

def reset_coil():
	i2c.writeto(0x30, b'\x00\x04')
	sleep(0.005)

def measure():
	i2c.writeto(0x30, b'\x00\x01')
	sleep(0.010)
	data = i2c.readfrom(0x30,5)
	return data

def do_connect():
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect('your SSID', 'your password')
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())

def compass():
	set_coil()
	reset_coil()
	data = measure()
	msb_x = data[0] & 0x0F
	lsb_x = data[1]
	msb_y = data[2] & 0x0F
	lsb_y = data[3]
	x = msb_x * 256 + lsb_x -2048
	y = msb_y * 256 + lsb_y -2048
	#print(x, y)
	w = atan2(y,x)/pi*180.0
	if w < 0:
		w = w + 360.0
	#print(w)
	return (w, x, y)


print("Compass sensor found at: 0x%02X" % (i2c.scan()[0]))

while True:	
	do_connect()
	print("sending data to Thingspeak")
	led.value(0)
	data = compass()
	print(data)
	c = data[0]	# heading
	x = data[1]	# mag. field x
	y = data[2]	# mag. field y

	data = b"api_key="+ API_KEY + "&field1=" + str(c) + "&field2=" + str(x) + "&field3=" + str(y)
      
        s = _socket.socket()
        ai = _socket.getaddrinfo(HOST, 443)
        addr = ai[0][-1]
        s.connect(addr)
        s = ssl.wrap_socket(s)
        s.write("POST /update HTTP/1.0\r\n")
        s.write("Host: " + HOST + "\r\n")
        s.write("Content-Length: " + str(len(data)) + "\r\n\r\n")
        s.write(data)
        print(s.read(128))
        s.close()
	led.value(1)
	sleep(15)

