from machine import Pin, PWM
import time

melody_buzzer = PWM(Pin(6, Pin.OUT), freq=100, duty=0)
melody_buzzer.duty(0)

key1 = Pin(38, Pin.IN, Pin.PULL_UP)
key2 = Pin(39, Pin.IN, Pin.PULL_UP)

try:
    while True:
        if key1.value() == 0 and key2.value() == 1:
            melody_buzzer.duty(512)
            melody_buzzer.freq(261)
        elif key1.value() == 1 and key2.value() == 0:
            melody_buzzer.duty(512)
            melody_buzzer.freq(293)
        elif key1.value() == 0 and key2.value() == 0:
            melody_buzzer.duty(512)
            melody_buzzer.freq(329)
        else:
            melody_buzzer.duty(0)
except:
    melody_buzzer.duty(0) 
