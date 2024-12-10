import ir_rx
import machine
import math, time

from machine import Pin, PWM, Timer, ADC
from ir_rx.nec import NEC_8 # Use the NEC 8-bit class
from ir_rx.print_error import print_error # for debugging

# load the MicroPython pulse-width-modulation module for driving hardware


time.sleep(1) # Wait for USB to become ready
delay = 0.1
pwm_rate = 2000

# MOTOR ALIGNMENT A = LEFT, B = RIGHT
#led1 = Pin(3, Pin.OUT)
#led2 = Pin(4, Pin.OUT)
#led3 = Pin(5, Pin.OUT)

motA_en = PWM(13, freq = pwm_rate, duty_u16 = 0)
motA_ph = Pin(12, Pin.OUT) # Initialize GP14 as an OUTPUT for motor A
motB_en = PWM(15, freq = pwm_rate, duty_u16 = 0)
motB_ph = Pin(14, Pin.OUT) # Initialize GP14 as an OUTPUT for motor A

# Low voltage battery setup
battery = ADC(Pin(27))
ledV = Pin(3, Pin.OUT)
ledV.off()                           # turn LED off
ledV.toggle()                        # turn LED on to know program is running

pwm = 20000

rf_p7 = Pin(7, Pin.IN, Pin.PULL_UP)
rf_p6 = Pin(6, Pin.IN, Pin.PULL_UP)
rf_p5 = Pin(5, Pin.IN, Pin.PULL_UP)
rf_p4 = Pin(4, Pin.IN, Pin.PULL_UP)
ir_pin = Pin(18, Pin.IN, Pin.PULL_UP) # Adjust the pin number based on your wiring
IR_transmit = 0
RF = 0
IR = 0 

# Callback function to execute when an IR code is received
# assuming motB.low() is forwards for B 
# motors get flipped across the robot so they need reverse polarity to go straight
def ir_callback(data, addr, _):
    
    #led1.toggle()
    #led2.toggle()
    #led3.toggle()
    #time.sleep(1)

    #if not IR_transmit:
    #   return
    
    print(f"Received NEC command! Data: 0x{data:02X}, Addr: 0x{addr:02X}")

    if (data == 0x02) & (IR_transmit):                 # drive forwards
        print("forwards")
        Forwards(pwm)
    elif (data == 0x01) & (IR_transmit):               # drive backwards
        print("backwards")
        Backwards(pwm)
    elif (data == 0x03) & (IR_transmit):               # turn right
        print("right")
        Right(pwm)
    elif (data == 0x04) & (IR_transmit):               # turn left
        print("left")

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


    #led1.off()
    #led2.off()
    #led3.off()


# Setup the IR receiver
ir_receiver = NEC_8(ir_pin, callback=ir_callback)


# Optional: Use the print_error function for debugging
ir_receiver.error_function(print_error)


#input 1 callback
def callback1(rf_p7):
    print("forwards")
    if RF:
        Forwards(pwm)
    
def callback2(rf_p6):
    print("backwards")
    if RF:  
        Backwards(pwm)


def callback3(rf_5):
    print("right")
    if RF:
        Right(pwm)


def callback4(rf_p4):
    print("left")
    if RF:
        Left(pwm)

rf_p7.irq(trigger=Pin.IRQ_RISING, handler=callback1)
rf_p6.irq(trigger=Pin.IRQ_RISING, handler=callback2)
rf_p5.irq(trigger=Pin.IRQ_RISING, handler=callback3)
rf_p4.irq(trigger=Pin.IRQ_RISING, handler=callback4)

#def checkADC(tim1):
 #   value = (3.3/65535) * battery.read_u16()    # convert ADC to legible voltage value
  #  print(value)
   # if(value < 3.119):               # value determined in testing
    #    while True:
     #       ledV.toggle()
      #      time.sleep(200)

#tim1 = Timer()
#tim1.init(period = 200, mode = Timer.PERIODIC, callback = checkADC) #timer interrupt to check the ADC ever 200 ms

def Forwards(pwm):
    motA_ph.high()
    motA_en.duty_u16(pwm)
    motB_ph.low()
    motB_en.duty_u16(pwm)
    time.sleep(delay)
    motA_en.duty_u16(0)
    motB_en.duty_u16(0)

def Backwards(pwm):
    motA_ph.low()
    motA_en.duty_u16(pwm)
    motB_ph.high()
    motB_en.duty_u16(pwm)
    time.sleep(delay)
    motA_en.duty_u16(0)
    motB_en.duty_u16(0)

def Right(pwm):
    motA_ph.low()
    motA_en.duty_u16(pwm)
    motB_ph.low()
    motB_en.duty_u16(pwm)
    time.sleep(delay)
    motA_en.duty_u16(0)
    motB_en.duty_u16(0)

def Left(pwm):
    motA_ph.high()
    motA_en.duty_u16(pwm)
    motB_ph.high()
    motB_en.duty_u16(pwm)
    time.sleep(delay)
    motA_en.duty_u16(0)
    motB_en.duty_u16(0)

# Main loop to keep the script running
while True:
    if IR:
        IR_transmit = 1
    else:
        IR_transmit = 0
# Execution is interrupt-driven, so just keep the script alive