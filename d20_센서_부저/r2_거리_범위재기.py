import machine
import time
from machine import Pin

trigger = Pin(17, mode=Pin.OUT, pull=None)
echo = Pin(1, mode=Pin.IN, pull=None)
trigger.value(0)

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

lo = 200                         # 지금까지 본 가장 가까운 거리 : 처음에는 아주 큰 값에서 시작한다
hi = 0                           # 지금까지 본 가장 먼 거리 : 처음에는 아주 작은 값에서 시작한다

try:
    while True:
        cm = get_distance_cm()
        if cm != 0:              # 0 은 못 읽은 것이니 건너뛴다
            if cm < lo:
                lo = cm
            if cm > hi:
                hi = cm
            print("지금", int(cm), "cm | 가장 가까움", int(lo), "| 가장 멈", int(hi))
        time.sleep(0.2)
except KeyboardInterrupt:
    print("내 거리 범위 : 가장 가까움", int(lo), "가장 멈", int(hi))
