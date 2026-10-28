import machine
import time
from machine import Pin, PWM

trigger = Pin(17, mode=Pin.OUT, pull=None)
echo = Pin(1, mode=Pin.IN, pull=None)
trigger.value(0)

melody_buzzer = PWM(Pin(6, Pin.OUT), freq=300, duty=0)
melody_buzzer.duty(0)

def get_distance_cm():
    trigger.value(0)
    time.sleep_us(5)
    trigger.value(1)
    time.sleep_us(10)
    trigger.value(0)

    pulse_time = machine.time_pulse_us(echo, 1, 30000)
    distance_cm = (pulse_time / 2) / 29.1
    if 2 <= distance_cm <= 200:
        return distance_cm
    else:
        return 0

try:
    while True:
        distance_cm = get_distance_cm()
        if 2 <= distance_cm <= 10:
            print(distance_cm,"cm")
            melody_buzzer.duty(512) 
            melody_buzzer.freq(300)
            time.sleep_ms(500)
        else:
            melody_buzzer.duty(0) 
        
        time.sleep(0.1)
        

except KeyboardInterrupt:
    melody_buzzer.duty(0) 


