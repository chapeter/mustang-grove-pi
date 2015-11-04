# GrovePi + Grove - LCD RGB Backlight
# http://www.seeedstudio.com/wiki/Grove_-_LCD_RGB_Backlight
#
# Just supports setting the backlight colour, and
# putting a single string of text onto the display
# Doesn't support anything clever, cursors or anything


import time,sys
import RPi.GPIO as GPIO
import smbus
import socket
import fcntl
import struct

# this device has two I2C addresses
DISPLAY_RGB_ADDR = 0x62
DISPLAY_TEXT_ADDR = 0x3e

# use the bus that matches your raspi version
rev = GPIO.RPI_REVISION
if rev == 2 or rev == 3:
    bus = smbus.SMBus(1)
else:
    bus = smbus.SMBus(0)

# set backlight to (R,G,B) (values from 0..255 for each)
def setRGB(r,g,b):
    bus.write_byte_data(DISPLAY_RGB_ADDR,0,0)
    bus.write_byte_data(DISPLAY_RGB_ADDR,1,0)
    bus.write_byte_data(DISPLAY_RGB_ADDR,0x08,0xaa)
    bus.write_byte_data(DISPLAY_RGB_ADDR,4,r)
    bus.write_byte_data(DISPLAY_RGB_ADDR,3,g)
    bus.write_byte_data(DISPLAY_RGB_ADDR,2,b)

# send command to display (no need for external use)    
def textCommand(cmd):
    bus.write_byte_data(DISPLAY_TEXT_ADDR,0x80,cmd)

# set display text \n for second line(or auto wrap)     
def setText(text):
    textCommand(0x01) # clear display
    time.sleep(.05)
    textCommand(0x08 | 0x04) # display on, no cursor
    textCommand(0x28) # 2 lines
    time.sleep(.05)
    count = 0
    row = 0
    for c in text:
        if c == '\n' or count == 16:
            count = 0
            row += 1
            if row == 2:
                break
            textCommand(0xc0)
            if c == '\n':
                continue
        count += 1
        bus.write_byte_data(DISPLAY_TEXT_ADDR,0x40,ord(c))

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])


# example code
if __name__=="__main__":
    hostname = socket.gethostname()
    try:
        wlan0_ipaddr = get_ip_address('wlan0')
#    setText('IP:\n%s' % (wlan0_ipaddr))
        setText('%s - wlan0\n%s' % (hostname, wlan0_ipaddr))
        setRGB(0,128,64)
    except:
        setText('No Wireless')
        setRGB(0,128,64)
	try:
            eth0_ipaddr = get_ip_address('eth0')
            setText('%s - eth0\n%s' % (hostname, eth0_ipaddr))
            setRGB(0,128,64)
        except:
            setText('No Wireless\nNoLAN')


    #for c in range(0,255):
    #    setRGB(c,255-c,0)
    #    time.sleep(0.01)
    #setRGB(0,255,0)
