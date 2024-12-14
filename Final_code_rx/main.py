import ir_rx
import machine
import math, time
import utime


from machine import I2C
from machine import Pin, PWM, Timer, ADC
from ir_rx.nec import NEC_8 # Use the NEC 8-bit class
from ir_rx.print_error import print_error # for debugging

# load the MicroPython pulse-width-modulation module for driving hardware

ENABLED = 1
DISABLED = 0

#timepassed = 0

last_movement_command_time = time.ticks_ms()

time.sleep(1) # Wait for USB to become ready
delay = 100
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
ledV.on()                           # turn LED off
# ledV.toggle()                        # turn LED on to know program is running

#ultrasonic sensor setup
i2c = I2C(0,sda=machine.Pin(0), scl=machine.Pin(1), freq=400000)
trigger = Pin(21, Pin.OUT)
echo = Pin(22, Pin.IN)


pwm = 22000
pwm2 = 28000


rf_p7 = Pin(7, Pin.IN, Pin.PULL_UP)
rf_p6 = Pin(6, Pin.IN, Pin.PULL_UP)
rf_p5 = Pin(5, Pin.IN, Pin.PULL_UP)
rf_p4 = Pin(4, Pin.IN, Pin.PULL_UP)
ir_pin = Pin(18, Pin.IN, Pin.PULL_UP) # Adjust the pin number based on your wiring
# IR_transmit = DISABLED
# RF = DISABLED
# IR = DISABLED
IR_transmit = 0
RF = 0
IR = 0

device_addr = 0xb7

# Callback function to execute when an IR code is received
# assuming motB.low() is forwards for B 
# motors get flipped across the robot so they need reverse polarity to go straight
def ir_callback(data, addr, _):
    global RF
    global IR    
    
    print(f"Received NEC command! Data: 0x{data:02X}, Addr: 0x{addr:02X}")

    if (data == 0x01) and (IR_transmit) and (device_addr == addr):                 # drive forwards
       # print("forwards")
        Forwards(pwm)
    elif (data == 0x02) and (IR_transmit) and (device_addr == addr):               # drive backwards
        #print("backwards")
        Backwards(pwm)
    elif (data == 0x03) and (IR_transmit) and (device_addr == addr):               # turn right
        #print("right")
        Right(pwm)
    elif (data == 0x04) and (IR_transmit) and (device_addr == addr):               # turn left
        #print("left")
        Left(pwm)

    elif (data == 0x05) and (device_addr == addr):
       # global RF
        #global IR
        # RF = DISABLED
        # IR = ENABLED
        RF = 0
        IR = 1
        print ("IR selected")
    elif (data == 0x06) and (device_addr == addr):
       # global RF
        #global IR
        # RF = ENABLED
        # IR = DISABLED
        RF = 1
        IR = 0
        print ("RF selected")        



# Setup the IR receiver
ir_receiver = NEC_8(ir_pin, callback=ir_callback)


# Optional: Use the print_error function for debugging
ir_receiver.error_function(print_error)



#input 1 callback
def callback1(rf_p7):
    if RF:    
        print("forwards")
        Forwards(pwm)
    
def callback2(rf_p6):
    if RF:  
        print("backwards")
        Backwards(pwm)


def callback3(rf_5):
    if RF:
        print("right")
        Right(pwm)


def callback4(rf_p4):
    if RF:
        print("left")
        Left(pwm)

rf_p7.irq(trigger=Pin.IRQ_RISING, handler=callback1)
rf_p6.irq(trigger=Pin.IRQ_RISING, handler=callback2)
rf_p5.irq(trigger=Pin.IRQ_RISING, handler=callback3)
rf_p4.irq(trigger=Pin.IRQ_RISING, handler=callback4)


def Forwards(pwm):
    print("forwards")
    global last_movement_command_time
    last_movement_command_time = time.ticks_ms()
    motA_ph.low()
    motA_en.duty_u16(pwm)
    motB_ph.high()
    motB_en.duty_u16(pwm)
    #time.sleep_ms(delay)


def Forwards_fast(pwm2):
    print("forwards fast")
    global last_movement_command_time
    last_movement_command_time = time.ticks_ms()
    motA_ph.low()
    motA_en.duty_u16(pwm2)
    motB_ph.high()
    motB_en.duty_u16(pwm2)
    #time.sleep_ms(100)


def Backwards(pwm):
    print("backwards")
    global last_movement_command_time
    last_movement_command_time = time.ticks_ms()
    motA_ph.high()
    motA_en.duty_u16(pwm)
    motB_ph.low()
    motB_en.duty_u16(pwm)
    #time.sleep_ms(delay)


def Right(pwm):
    print("right")
    global last_movement_command_time
    last_movement_command_time = time.ticks_ms()
    motA_ph.low()
    motA_en.duty_u16(pwm)
    motB_ph.low()
    motB_en.duty_u16(pwm)
    #time.sleep_ms(delay)


def Left(pwm):
    print("left")
    global last_movement_command_time
    last_movement_command_time = time.ticks_ms()
    motA_ph.high()
    motA_en.duty_u16(pwm)
    motB_ph.high()
    motB_en.duty_u16(pwm)
    #time.sleep_ms(delay)

def Stop():
    motA_en.duty_u16(0)
    motB_en.duty_u16(0)
   # time.sleep_ms(delay)


def ultra():
    trigger.low()
    utime.sleep_us(2)
    trigger.high()
    utime.sleep_us(5)
    trigger.low()
    timeout= utime.ticks_us() + 30000
    signaloff = signalon = utime.ticks_us()
    while echo.value() == 0 and utime.ticks_us() < timeout:
        signaloff = utime.ticks_us()
    while echo.value() == 1 and utime.ticks_us() < timeout:
        signalon = utime.ticks_us()
    if signalon <= signaloff:
        return "No Echo Recieved"
    timepassed = utime.ticks_diff(signalon,signaloff)
    distance = (timepassed * 0.0343) / 2
    # if distance > 30:
    #     output = "No Object Detected!"
    #     print(output)
    #     print("No Object Detected")
        
    if (distance < 25 ) and (distance > 0):
        output = "Object detected!",distance,"cm"
        print(output)
        print("Object detected!")
        print("%s cm" % distance)
        Forwards_fast(pwm2)
#     #while True:
#         #ultra()
#         #utime.sleep(5)
#         #utime.sleep(1)

# def ultra():
#     # Ensure trigger is low initially
#     trigger.low()
#     utime.sleep_us(2)
    
#     # Send a 10-microsecond pulse
#     trigger.high()
#     utime.sleep_us(5)
#     trigger.low()
    
#     # Wait for the echo signal to start
#     timeout = utime.ticks_us() + 30000  # 30 ms timeout
#     while echo.value() == 0:
#         if utime.ticks_us() > timeout:
#             print("No Echo Received")
#             return "No Echo Received"
#         signaloff = utime.ticks_us()

#     # Wait for the echo signal to stop
#     while echo.value() == 1:
#         if utime.ticks_us() > timeout:
#             print("Echo Timeout")
#             return "Echo Timeout"
#         signalon = utime.ticks_us()
    
#     # Calculate the duration of the echo pulse
#     timepassed = utime.ticks_diff(signalon, signaloff)

#     # Convert time to distance (speed of sound = 343 m/s or 0.0343 cm/us)
#     distance = (timepassed * 0.0343) / 2  # Divide by 2 for round trip

#     # Check distance and provide feedback
#     if distance > 30:
#         print("No Object Detected!")
#         return "No Object Detected!"
#     elif (distance < 30 ) and (distance > 0):
#         print(f"Object detected! Distance: {distance:.2f} cm")
#         return f"Object detected! Distance: {distance:.2f} cm"


# Main loop to keep the script running
while True:
    current_time = time.ticks_ms()
    if (time.ticks_diff(current_time, last_movement_command_time) > delay):
        print("TimeDiff", time.ticks_diff(time.ticks_ms(), last_movement_command_time))
        Stop()

    if IR:
        IR_transmit = 1
    else:
        IR_transmit = 0

    
    
    # if (IR == ENABLED):
    #     IR_transmit = ENABLED
    #     ledV.on()
    # else:
    #     IR_transmit = DISABLED
    #     ledV.off()

    # if (IR == ENABLED):
    #     pass
    #     # ledV.on()
    # else:
    #     pass
    #     # ledV.off()

    utime.sleep_ms(500)
    ultra()
    ledV.toggle()
# Execution is interrupt-driven, so just keep the script alive