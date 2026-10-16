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
        if 2 <= distance_cm < 4:
            melody_buzzer.freq(261)  # 도
            melody_buzzer.duty(512)
            time.sleep_ms(200) 
        elif 4 <= distance_cm < 6:
            melody_buzzer.freq(293)  # 레
            melody_buzzer.duty(512)
            time.sleep_ms(200) 
        elif 6 <= distance_cm < 8:
            melody_buzzer.freq(329)  # 미
            melody_buzzer.duty(512)
            time.sleep_ms(200) 
        elif 8 <= distance_cm < 10:
            melody_buzzer.freq(349)  # 파
            melody_buzzer.duty(512)
            time.sleep_ms(200) 
        elif 10 <= distance_cm < 12:
            melody_buzzer.freq(392)  # 솔
            melody_buzzer.duty(512)
            time.sleep_ms(200) 
        elif 12 <= distance_cm < 14:
            melody_buzzer.freq(440)  # 라
            melody_buzzer.duty(512)
            time.sleep_ms(200) 
        elif 14 <= distance_cm < 16:
            melody_buzzer.freq(493)  # 시
            melody_buzzer.duty(512)
            time.sleep_ms(200) 
        elif 16 <= distance_cm <= 18:
            melody_buzzer.freq(523)  # 높은 도
            melody_buzzer.duty(512)
            time.sleep_ms(200) 
        else:
            melody_buzzer.duty(0) 
        
        time.sleep(0.1)
        

except KeyboardInterrupt:
    melody_buzzer.duty(0) 



