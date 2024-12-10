

import ir_rx
import machine
import math, time

from machine import Pin
from machine import PWM
from ir_rx.nec import NEC_8 # Use the NEC 8-bit class
from ir_rx.print_error import print_error # for debugging

# load the MicroPython pulse-width-modulation module for driving hardware


time.sleep(1) # Wait for USB to become ready

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
    