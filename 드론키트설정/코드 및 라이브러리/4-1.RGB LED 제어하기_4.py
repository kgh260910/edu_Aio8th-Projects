from machine import Pin, PWM
import time

LED_RED = PWM(Pin(21), freq=1000, duty=0)
LED_GREEN = PWM(Pin(47), freq=1000, duty=0)
LED_BLUE = PWM(Pin(48), freq=1000, duty=0)

rainbow_colors = [
    (1023, 0, 0),     
    (1023, 200, 0),   
    (1023, 400, 0),   
    (0, 1023, 0),     
    (0, 0, 1023),     
    (200, 0, 1023),   
    (400, 0, 1023),   
]

while True:
    for color in rainbow_colors:
        LED_RED.duty(color[0])
        LED_GREEN.duty(color[1])
        LED_BLUE.duty(color[2])
        time.sleep(1.0)