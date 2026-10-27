import machine
import time
from machine import Pin, PWM, Timer

buzzer = PWM(Pin(6), freq=880, duty=0)
trigger = Pin(17, mode=Pin.OUT, pull=None)
echo = Pin(1, mode=Pin.IN, pull=None)
trigger.value(0)

# ---- 내가 바꾸는 값 (s2_거리_소리.py 와 같다) ----
NEAR_CM = 5
FAR_CM = 40
LEVELS = 20
DUTY_TABLE = [10, 12, 15, 19, 23, 28, 35, 43, 52, 65, 79, 98, 120, 148, 182, 224, 275, 338, 416, 512]

# ---- 인터럽트 깃발 : 알람 ----
ms = 0
flag_10 = False
flag_50 = False
flag_500 = False

def tick(t):
    global ms, flag_10, flag_50, flag_500
    ms += 1
    if ms % 10 == 0:
        flag_10 = True
    if ms % 50 == 0:
        flag_50 = True
    if ms % 500 == 0:
        flag_500 = True

def get_distance_cm():           # 교재 5-3 _2 와 같은 함수 : 못 읽으면 0
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

def distance_level(cm):          # s2 와 같은 함수
    level = (FAR_CM - cm) * LEVELS // (FAR_CM - NEAR_CM) + 1
    return max(1, min(LEVELS, int(level)))

beep_on = False
cm = 0
level = 10
duty = DUTY_TABLE[level - 1]
last_look = 0                    # 거리를 마지막으로 본 ms
look_gap = 0                     # 거리를 다시 보기까지 걸린 ms

tmr = Timer(0)
tmr.init(period=1, mode=Timer.PERIODIC, callback=tick)

try:
    while True:
        if flag_10:                              # 10 ms : 소리 크기를 부저에 반영한다
            flag_10 = False
            if beep_on:
                buzzer.duty(duty)
            else:
                buzzer.duty(0)
        if flag_50:                              # 50 ms : 거리를 잰다
            flag_50 = False
            cm = get_distance_cm()
            if cm != 0:                          # 0 은 못 읽은 것 : 이전 단계를 그대로 쓴다
                level = distance_level(cm)
                duty = DUTY_TABLE[level - 1]
            look_gap = ms - last_look
            last_look = ms
        if flag_500:                             # 500 ms : 삑을 켜고 끄고, 쉘에 찍는다
            flag_500 = False
            beep_on = not beep_on
            print("거리", int(cm), "cm -> 단계", level, "-> duty", duty, "| 센서를 다시 보기까지", look_gap, "ms")
except KeyboardInterrupt:
    pass
finally:
    tmr.deinit()
    buzzer.duty(0)
    buzzer.deinit()
