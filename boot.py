# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
# Complete project details at https://RandomNerdTutorials.com
try:
  import usocket as socket
except:
  import socket

from machine import Pin, ADC
import network

from WIFI_CREDENTIALS import ssid, password


import esp
esp.osdebug(None)

import gc
gc.collect()


wlan = network.WLAN(network.STA_IF) # create station interface
wlan.active(False)
wlan.active(True)       # activate the interface
wlan.ifconfig(("192.168.1.187", "255.255.255.0", "192.168.1.1", "192.168.1.1"))
wlan.connect(ssid, password) # connect to an AP

while wlan.isconnected() == False:
  pass

print('Connection successful')
print(wlan.ifconfig())

led = Pin(2, Pin.OUT)
relay = Pin(4, Pin.OUT)
analogPin = ADC(0)