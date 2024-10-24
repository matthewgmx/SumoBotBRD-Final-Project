#   Pico pin GP13   -> AIN2
#   Pico pin GP12   -> AIN1
#   any Pico GND    -> GND

import math, time
import machine
# load the MicroPython pulse-width-modulation module for driving hardware
from machine import PWM

from machine import Pin

time.sleep(1) # Wait for USB to become ready

pwm_rate = 2000

#MOTOR ALIGNMENT A = LEFT, B = RIGHT
motA_ph = Pin(12, Pin.OUT) # Initialize GP14 as an OUTPUT for motor A
motB_ph = Pin(11, Pin.OUT) # Initialize GP14 as an OUTPUT for motor B
motA_en = PWM(13, freq = pwm_rate, duty_u16 = 0)
motB_en = PWM(14, freq = pwm_rate, duty_u16 = 0)
pwm = 5000

#DRIVE LOOP
while True:
    #FORWARDS CONTROL (BOTH HI)
    print("Motor A Forwards") # Print to REPL
    print("Motor B Forwards") # Print to REPL
    motA_ph.high()
    motB_ph.high()
    motA_en.duty_u16(pwm)
    motB_en.duty_u16(pwm)
    time.sleep(2)
    print("Motors OFF") # Print to REPL
    motA_en.duty_u16(0)
    motB_en.duty_u16(0)
    time.sleep(2)

    # BACKWARDS CONTROL (BOTH LO)
    print("Backwards") # Print to REPL
    motA_ph.low()
    motB_ph.low()
    motA_en.duty_u16(pwm)
    motB_en.duty_u16(pwm) 
    time.sleep(2)
    print("Motor OFF") # Print to REPL
    motA_en.duty_u16(0)
    motB_en.duty_u16(0)
    time.sleep(2)

    #TURN LEFT (LEFT LO, RIGHT HI)
    print("Turn Left")
    print("Backwards") # Print to REPL
    motA_ph.low()
    motB_ph.high()
    motA_en.duty_u16(pwm)
    motB_en.duty_u16(pwm) 
    time.sleep(2)
    print("Motor OFF") # Print to REPL
    motA_en.duty_u16(0)
    motB_en.duty_u16(0)
    time.sleep(2)

    #TURN RIGHT (LEFT HI, RIGHT LO)
    motA_ph.high()
    motB_ph.low()
    motA_en.duty_u16(pwm)
    motB_en.duty_u16(pwm)
    time.sleep(2)
    print("Motors OFF") # Print to REPL
    motA_en.duty_u16(0)
    motB_en.duty_u16(0)
    time.sleep(2)

