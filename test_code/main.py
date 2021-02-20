#DRV8825 temporary test board

from machine import Pin
from pyb import CAN
import utime


# Needed inputs/ outputs

# Left side:
# set_position
# set_offset example: @some_value saw cuts a 50mm piece
# go_home
# set_speed
# set_acceleration
# set_positive_direction
# set_steps_per_millimeter = 13.3333333
# inactivity_timeout  example: turns off motor after set amount of time


# Right Side:
# is_homed
# low_limit_switch
# high_limit_switch
# motor_is_enabled


move_delay = 450


HBT_LED = Pin("D13", Pin.OUT)
FUNC_BUTTON = Pin("D5", Pin.IN, Pin.PULL_UP) 

DIR_PIN = Pin("A0", Pin.OUT)
STEP_PIN = Pin("A2", Pin.OUT)
ENABLE_PIN = Pin("A4", Pin.OUT)
LIMIT_PIN = Pin("D0", Pin.IN, Pin.PULL_UP)


DIR_PIN.value(0) #set initial direction
ENABLE_PIN.value(1) #turn motor driver off

    #Setup hbt timer
hbt_state = 0
hbt_interval = 500
start = utime.ticks_ms()
next_hbt = utime.ticks_add(start, hbt_interval)
HBT_LED.value(hbt_state)


print("starting Devboard")


def chk_hbt():
    global next_hbt
    global hbt_state
    now = utime.ticks_ms()
    if utime.ticks_diff(next_hbt, now) <= 0:
        if hbt_state == 1:
            hbt_state = 0
            HBT_LED.value(hbt_state)
            #print("hbt")
        else:
            hbt_state = 1
            HBT_LED.value(hbt_state)  
        
        next_hbt = utime.ticks_add(next_hbt, hbt_interval)

def enable():
    ENABLE_PIN.value(0)
    
def disable():
    ENABLE_PIN.value(1)
    
def move():
    print("doing move thing")
    DIR_PIN.value(1)
    enable()
    utime.sleep_ms(1)
    for i in range(4800):
        STEP_PIN.value(1)
        #utime.sleep_ms(move_delay)
        STEP_PIN.value(0)
        utime.sleep_us(move_delay)
    DIR_PIN.value(0)
    utime.sleep_ms(1)
    for i in range(4800):
        STEP_PIN.value(1)
        #utime.sleep_ms(move_delay)
        STEP_PIN.value(0)
        utime.sleep_us(move_delay)
    disable()
        
while True:
    chk_hbt()
    if not (FUNC_BUTTON.value()):
        print("function button")
        utime.sleep_ms(200)
    if (LIMIT_PIN.value()):
        print("limit switch")
        move()
        utime.sleep_ms(500)