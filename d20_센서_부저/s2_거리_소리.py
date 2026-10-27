import machine
import time
from machine import Pin, PWM

buzzer = PWM(Pin(6), freq=880, duty=0)
trigger = Pin(17, mode=Pin.OUT, pull=None)
echo = Pin(1, mode=Pin.IN, pull=None)
trigger.value(0)

# ---- 내가 바꾸는 값 : r2_거리_범위재기.py 로 잰 내 값을 넣는다 ----
NEAR_CM = 5                      # 손을 가장 가까이 둘 때의 거리 (가장 큰 소리)
FAR_CM = 40                      # 손을 가장 멀리 둘 때의 거리 (가장 작은 소리) : NEAR_CM 보다 커야 한다
LEVELS = 20                      # 소리 크기를 몇 단계로 나눌까
# 단계 1~20 -> duty : 약 1 % (10) 에서 50 % (512) 까지, 앞쪽은 촘촘하고 뒤쪽은 성기게
DUTY_TABLE = [10, 12, 15, 19, 23, 28, 35, 43, 52, 65, 79, 98, 120, 148, 182, 224, 275, 338, 416, 512]
BEEP_MS = 500
REST_MS = 500

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

def distance_level(cm):
    # 가까울수록 큰 단계 : NEAR_CM 이하 -> 20, FAR_CM 이상 -> 1
    level = (FAR_CM - cm) * LEVELS // (FAR_CM - NEAR_CM) + 1
    return max(1, min(LEVELS, int(level)))

def beep(duty):
    buzzer.duty(duty)
    time.sleep_ms(BEEP_MS)
    buzzer.duty(0)
    time.sleep_ms(REST_MS)

level = 10                       # 처음 단계 (못 읽어도 소리 나게)
last_look = time.ticks_ms()

try:
    while True:
        cm = get_distance_cm()
        if cm != 0:                              # 0 은 못 읽은 것 : 이전 단계를 그대로 쓴다
            level = distance_level(cm)
        duty = DUTY_TABLE[level - 1]
        now = time.ticks_ms()
        gap = time.ticks_diff(now, last_look)
        last_look = now
        print("거리", int(cm), "cm -> 단계", level, "-> duty", duty, "| 센서를 다시 보기까지", gap, "ms")
        beep(duty)
except KeyboardInterrupt:
    pass
finally:
    buzzer.duty(0)
    buzzer.deinit()
