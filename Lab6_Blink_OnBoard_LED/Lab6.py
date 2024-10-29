from machine import Pin
from utime import sleep

pin = Pin(3, Pin.OUT)
pin1 = Pin(4, Pin.OUT)
pin2 = Pin(5, Pin.OUT)



print("LED starts flashing...")
while True:
    try:
        pin.toggle()
        pin1.toggle()
        pin2.toggle()
        sleep(1)
    except KeyboardInterrupt:
        break
pin.off()
pin2.off()
pin1.off()
print("Finished.")

