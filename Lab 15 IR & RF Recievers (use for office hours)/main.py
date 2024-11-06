import ir_rx
import machine
import math, time

from machine import Pin
from machine import PWM
from ir_rx.nec import NEC_8 # Use the NEC 8-bit class
from ir_rx.print_error import print_error # for debugging

#       ***The problems we are having***
#       The RF reciever is recieving signals from the remote but the code is not written properly to react to this
#       It does not appear that our callback functions for the RF reciever are being triggered

# load the MicroPython pulse-width-modulation module for driving hardware


time.sleep(1) # Wait for USB to become ready

pwm_rate = 2000

# MOTOR ALIGNMENT A = LEFT, B = RIGHT
led1 = Pin(3, Pin.OUT)
led2 = Pin(4, Pin.OUT)
led3 = Pin(5, Pin.OUT)

motA_en = PWM(13, freq = pwm_rate, duty_u16 = 0)
motA_ph = Pin(12, Pin.OUT) # Initialize GP14 as an OUTPUT for motor A
motB_en = PWM(14, freq = pwm_rate, duty_u16 = 0)
motB_ph = Pin(11, Pin.OUT) # Initialize GP14 as an OUTPUT for motor A


pwm = 50000

rf_p18 = Pin(18, Pin.IN, Pin.PULL_UP)
rf_p19 = Pin(19, Pin.IN, Pin.PULL_UP)
rf_p20 = Pin(20, Pin.IN, Pin.PULL_UP)
rf_p21 = Pin(21, Pin.IN, Pin.PULL_UP)
IR_transmit = 0
RF = 0
IR = 0 

# Callback function to execute when an IR code is received
# assuming motB.low() is forwards for B 
# motors get flipped across the robot so they need reverse polarity to go straight
def ir_callback(data, addr, _):
    
    
    led1.toggle()
    led2.toggle()
    led3.toggle()
    time.sleep(1)

    #if not IR_transmit:
    #   return
    
    print(f"Received NEC command! Data: 0x{data:02X}, Addr: 0x{addr:02X}")

    if (data == 0x01) & (IR_transmit):                 # drive forwards
        print("forwards")
        motA_ph.high()
        motA_en.duty_u16(pwm)
        motB_ph.low()
        motB_en.duty_u16(pwm)
        time.sleep(1)
        motA_en.duty_u16(0)
        motB_en.duty_u16(0)
    elif (data == 0x02) & (IR_transmit):               # drive backwards
        print("backwards")
        motA_ph.low()
        motA_en.duty_u16(pwm)
        motB_ph.high()
        motB_en.duty_u16(pwm)
        time.sleep(1)
        motA_en.duty_u16(0)
        motB_en.duty_u16(0)
    elif (data == 0x03) & (IR_transmit):               # turn right
        print("right")
        motA_ph.low()
        motA_en.duty_u16(pwm)
        motB_ph.low()
        motB_en.duty_u16(pwm)
        time.sleep(1)
        motA_en.duty_u16(0)
        motB_en.duty_u16(0)
    elif (data == 0x04) & (IR_transmit):               # turn left
        print("left")
        motA_ph.high()
        motA_en.duty_u16(pwm)
        motB_ph.high()
        motB_en.duty_u16(pwm)
        time.sleep(1)
        motA_en.duty_u16(0)
        motB_en.duty_u16(0)
    elif (data == 0x05):
        global RF
        global IR
        RF = 0
        IR = 1
        print ("IR selected")
    elif (data == 0x06):
        global RF
        global IR
        RF = 1
        IR = 0
        print ("RF selected")        


    led1.off()
    led2.off()
    led3.off()


# Setup the IR receiver
ir_pin = Pin(17, Pin.IN, Pin.PULL_UP) # Adjust the pin number based on your wiring
ir_receiver = NEC_8(ir_pin, callback=ir_callback)


# Optional: Use the print_error function for debugging
ir_receiver.error_function(print_error)

#input 1 callback
def callback1(rf_p18):
    if not IR_transmit:
        motA_ph.high()
        motA_en.duty_u16(pwm)
        motB_ph.low()
        motB_en.duty_u16(pwm)
        time.sleep(1)
        motA_en.duty_u16(0)
        motB_en.duty_u16(0)
    rf_p18.irq(trigger=Pin.IRQ_RISING, handler=callback1)

def callback2(rf_p19):
    if not IR_transmit:
        print("backwards")
        motA_ph.low()
        motA_en.duty_u16(pwm)
        motB_ph.high()
        motB_en.duty_u16(pwm)
        time.sleep(1)
        motA_en.duty_u16(0)
        motB_en.duty_u16(0)
    rf_p19.irq(trigger=Pin.IRQ_RISING, handler=callback2)

def callback3(rf_p20):
    if not IR_transmit:
        print("right")
        motA_ph.low()
        motA_en.duty_u16(pwm)
        motB_ph.low()
        motB_en.duty_u16(pwm)
        time.sleep(1)
        motA_en.duty_u16(0)
        motB_en.duty_u16(0)
    rf_p20.irq(trigger=Pin.IRQ_RISING, handler=callback3)

def callback4(rf_p21):
    if not IR_transmit:
        print("left")
        motA_ph.high()
        motA_en.duty_u16(pwm)
        motB_ph.high()
        motB_en.duty_u16(pwm)
        time.sleep(1)
        motA_en.duty_u16(0)
        motB_en.duty_u16(0)
    rf_p21.irq(trigger=Pin.IRQ_RISING, handler=callback4)

# Main loop to keep the script running
while True:
    if IR:
        IR_transmit = 1
    else:
        IR_transmit = 0
# Execution is interrupt-driven, so just keep the script alive