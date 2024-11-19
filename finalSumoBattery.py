import machine
import math, time

from machine import Pin, ADC

time.sleep(1)
battery = ADC(Pin(27))
led = Pin(15, Pin.OUT)

led.off()                           # turn LED off
led.toggle()                        # turn LED on to know program is running

#def battery_callback(battery):
    #while True:
     #   led.toggle()
      #  time.sleep(0.1)

#value = (3.3/65535) * battery.read_u16()
    
#battery.irq(trigger = value < 3.13 , handler = battery_callback)

while True:
    value = (3.3/65535) * battery.read_u16()
    print("Battery level: ", value)
    time.sleep(0.25)
    if(value < 3.11):
        led.toggle()                # flash LED to alert low voltage