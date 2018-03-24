# Wemos D1 mini with e+e C02 sensor EE871
# E+E 2 beam infrared cell, 0 ... 5000 ppm
# distribute data via Thingspeak
# Channel ID: <channel id>
# Field 1: CO2 value 60 s response time
# Field 2: CO2 value 105 s response time
#
# connection:
# 1	brown	GND
# 2	white	+UB
# 3	blue	DATA
# 4 	black	CLOCK
#
# The sensor is communicating via E2 interface (slow I2C, clock max is 1000Hz) 
#
# SCL	D1 (wemos d1 mini)
# SDA	D2 (wemos d1 mini)


from machine import Pin,I2C
from utime import sleep
import network
import ussl as ssl
import usocket as _socket
import ussl as ssl

led=Pin(2,Pin.OUT)
led.value(1)
i2c=I2C(scl=Pin(5), sda=Pin(4), freq=1000)

API_KEY = "your write api key"
HOST = "api.thingspeak.com"

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

def getType():
	low = i2c.readfrom(0x08,1)[0]
	high = i2c.readfrom(0x20,1)[0]
	SensorType = high * 256 + low
	return SensorType

# fast measurement for handheld applications
def CO2_M3():
	low = i2c.readfrom(0x60,1)[0]
	high = i2c.readfrom(0x68,1)[0]
	CO2 = high * 256 + low
	return (CO2)

# slow measurement for climate control applications
def CO2_M4():
	low = i2c.readfrom(0x70,1)[0]
	high = i2c.readfrom(0x78,1)[0]
	CO2 = high * 256 + low
	return (CO2)


while True:	
	do_connect()

	print("sending data to Thingspeak")
	led.value(0)
	data = CO2_M3()
	print("CO2 60 s data", data)
	x = data	# CO2 value
	data = CO2_M4()
	print("CO2 105 s data", data)
	y = data	# CO2 value

	data = b"api_key="+ API_KEY + "&field1=" + str(x) + "&field2=" + str(y)      
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
	sleep(60)

