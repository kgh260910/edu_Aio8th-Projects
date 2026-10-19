from machine import Pin,PWM
import time

LED_RED = PWM(Pin(21),freq=1000,duty=0)
LED_GREEN = PWM(Pin(47),freq=1000,duty=0)
LED_BLUE = PWM(Pin(48),freq=1000,duty=0)

while True:
    LED_RED.duty(0)
    time.sleep(1.0)
    
    LED_RED.duty(400)
    time.sleep(1.0)
    
    LED_RED.duty(800)
    time.sleep(1.0)
    
    LED_RED.duty(1023)
    time.sleep(1.0)
