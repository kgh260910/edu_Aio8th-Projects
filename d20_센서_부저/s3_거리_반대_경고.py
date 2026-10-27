import machine
import time
from machine import Pin, PWM

buzzer = PWM(Pin(6), freq=880, duty=0)
trigger = Pin(17, mode=Pin.OUT, pull=None)
echo = Pin(1, mode=Pin.IN, pull=None)
trigger.value(0)

# ---- 내가 바꾸는 값 ----
NEAR_CM = 5                      # 손을 가장 가까이 둘 때의 거리 (가장 작은 소리)
WARN_CM = 60                     # 이 거리보다 멀면 삐~ 하고 길게 울린다 (경고)
LEVELS = 20                      # 소리 크기를 몇 단계로 나눌까
# 단계 0~19 -> duty : 약 1 % (10) 에서 약 15 % (150) 까지 (s2 와 같은 표)
DUTY_TABLE = [10, 12, 13, 15, 18, 20, 24, 27, 31, 36, 42, 48, 55, 64, 73, 85, 98, 113, 130, 150]
BEEP_FREQ = 880                  # 삑 소리의 높이
WARN_FREQ = 1760                 # 경고 삐~ 소리의 높이 : 삑보다 한 옥타브 높다
WARN_DUTY = 150                  # 경고 삐~ 소리의 크기 (가장 큰 삑과 같다)
WARN_MS = 600                    # 삐~ 를 한 번에 울리는 시간
MUTE_MS = 60                     # 삐~ 뒤에 소리를 끄고 기다리는 시간 : 소리가 나는 중에 재면 부저가 센서를 흔든다
FAR_LIMIT = 2                    # 멀다고 연속 몇 번 나오면 경고를 울릴까 (한 번 튄 값은 무시)
BEEP_MS = 500
REST_MS = 500

def get_distance_cm():           # 교재 5-3 _2 와 거의 같은 함수 : 못 읽거나 약 100 cm 보다 멀면 999
    trigger.value(0)
    time.sleep_us(5)
    trigger.value(1)
    time.sleep_us(10)
    trigger.value(0)
    # 6000 µs (약 100 cm) 까지만 기다린다 : 오래 기다리면 그동안 타이머 틱을 놓친다 (교재는 30000)
    pulse_time = machine.time_pulse_us(echo, 1, 6000)
    if pulse_time < 0:           # 반사가 돌아오지 않았다 = 앞이 비었다 = 아주 멀다
        return 999
    distance_cm = (pulse_time / 2) / 29.1
    if distance_cm > 100:
        return 999
    if distance_cm < 2:
        return 2
    return distance_cm

def distance_level(cm):
    # 가까울수록 작은 단계 (s2 와 반대) : NEAR_CM 이하 -> 0, WARN_CM 에 가까울수록 -> 19
    level = int((cm - NEAR_CM) * LEVELS // (WARN_CM - NEAR_CM))
    if level < 0:
        level = 0
    if level > LEVELS - 1:
        level = LEVELS - 1
    return level

def beep(duty):
    buzzer.freq(BEEP_FREQ)
    buzzer.duty(duty)
    time.sleep_ms(BEEP_MS)
    buzzer.duty(0)
    time.sleep_ms(REST_MS)

def warning():                   # 삐~ : 길게 울린 뒤 잠깐 끈다 (끈 직후에 거리를 재야 부저가 센서를 흔들지 않는다)
    buzzer.freq(WARN_FREQ)
    buzzer.duty(WARN_DUTY)
    time.sleep_ms(WARN_MS)
    buzzer.duty(0)
    time.sleep_ms(MUTE_MS)

far_count = 0                    # 멀다고 연속으로 나온 횟수

try:
    while True:
        cm = get_distance_cm()
        if cm > WARN_CM:
            far_count += 1
        else:
            far_count = 0
        if far_count >= FAR_LIMIT:               # 60 cm 보다 멀다 -> 삐~
            print("거리", int(cm), "cm -> 60 cm 보다 멀다 : 삐~")
            warning()
        else:                                    # 60 cm 안쪽 -> 가까울수록 작은 삑
            level = distance_level(cm)
            duty = DUTY_TABLE[level]
            print("거리", int(cm), "cm -> 단계", level, "-> duty", duty)
            beep(duty)
except KeyboardInterrupt:
    pass
finally:
    buzzer.duty(0)
    buzzer.deinit()
