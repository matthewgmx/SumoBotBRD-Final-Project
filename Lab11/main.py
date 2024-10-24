
import ir_rx
import machine
import math, time

from machine import Pin
from machine import PWM
from ir_rx.nec import NEC_8 # Use the NEC 8-bit class
from ir_rx.print_error import print_error # for debugging

# load the MicroPython pulse-width-modulation module for driving hardware


time.sleep(1) # Wait for USB to become ready

pwm_rate = 2000

#MOTOR ALIGNMENT A = LEFT, B = RIGHT
motA_ph = Pin(5, Pin.OUT) # Initialize GP14 as an OUTPUT for motor A
motA_en = PWM(4, freq = pwm_rate, duty_u16 = 0)
pwm = 5000


# Callback function to execute when an IR code is received
def ir_callback(data, addr, _):
    
    print(f"Received NEC command! Data: 0x{data:02X}, Addr: 0x{addr:02X}")

# Setup the IR receiver
ir_pin = Pin(17, Pin.IN, Pin.PULL_UP) # Adjust the pin number based on your wiring
ir_receiver = NEC_8(ir_pin, callback=ir_callback)

# Optional: Use the print_error function for debugging
ir_receiver.error_function(print_error)

# Main loop to keep the script running
while True:
    pass # Execution is interrupt-driven, so just keep the script alive
    
    if Data == 0x01 | Data == 0x02 | Data == 0x03 | Data == 0x04:
        motA_ph.high()
        motA_en.duty_u16(pwm)
    









# DRIVE FORWARDS (MA FORWARDS MB FORWARDS)


# DRIVE BACKWARDS (MA BACKWARDS MB BACKWARDS)

# TURN RIGHT(MA FORWARDS, MB BACKWARDS)

# TURN LEFT (MA BACKWARDS, MB FORWARDS)




