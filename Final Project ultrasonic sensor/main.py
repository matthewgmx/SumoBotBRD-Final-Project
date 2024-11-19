import utime
from machine import Pin
import machine
from machine import I2C


i2c = I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=400000)

    
trigger = Pin(21, Pin.OUT)
echo = Pin(22, Pin.IN)
def ultra():
   trigger.low()
   utime.sleep_us(2)
   trigger.high()
   utime.sleep_us(5)
   trigger.low()
   while echo.value() == 0:
       signaloff = utime.ticks_us()
   while echo.value() == 1:
       signalon = utime.ticks_us()
   timepassed = signalon - signaloff
   distance = (timepassed * 0.0343) / 2
   if distance > 30:
       output = "No Object Detected!"
       print(output)
       print("No Object Detected")
    
   else:
       output = "Object detected!",distance,"cm"
       print(output)
       print("Object detected!")
       print("%s cm" % distance)
while True:
   ultra()
   utime.sleep(5)
   utime.sleep(1)