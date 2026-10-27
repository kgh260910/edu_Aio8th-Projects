import machine                                  # machine : 보드의 부품(핀·타이머 등)을 다루는 도구 모음
import time                                     # time : 기다리거나 시간을 다루는 도구 모음
from machine import Pin, PWM                    # machine 에서 부품 도구(클래스)를 가져온다 : Pin(핀), PWM(부저)

# 부저 객체 만들기 : PWM 클래스(설계도)로 buzzer 를 만든다
#   Pin(6) = 6번 핀에 달린 부저, freq=880 = 소리 높이 880 Hz, duty=0 = 처음에는 소리 끔 (0~1023)
buzzer = PWM(Pin(6), freq=880, duty=0)
# trigger 객체 만들기 : Pin 클래스로 17번 핀을 쓴다. mode=Pin.OUT = 내보내는 핀(소리를 쏘라는 신호), pull=None = 내부 저항은 안 쓴다
trigger = Pin(17, mode=Pin.OUT, pull=None)
# echo 객체 만들기 : 1번 핀. mode=Pin.IN = 받는 핀(돌아온 소리 신호), pull=None = 내부 저항은 안 쓴다
echo = Pin(1, mode=Pin.IN, pull=None)
trigger.value(0)                                # value() 메서드 : 핀 값을 정한다. 0 = 끔 (처음에는 소리를 쏘지 않는다)

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
    trigger.value(0)                            # value(0) : 끈 상태에서 시작
    time.sleep_us(5)                            # sleep_us() : 5 µs 기다린다 (µs = 마이크로초 = 100만분의 1초)
    trigger.value(1)                            # value(1) : 켠다 = 초음파를 쏘기 시작
    time.sleep_us(10)                           # 10 µs 동안 켜 둔다
    trigger.value(0)                            # value(0) : 끈다 = 쏘기를 끝낸다
    # 6000 µs (약 100 cm) 까지만 기다린다 : 오래 기다리면 그동안 타이머 틱을 놓친다 (교재는 30000)
    pulse_time = machine.time_pulse_us(echo, 1, 6000)  # time_pulse_us(핀, 1, 최대µs) : echo 가 켜져 있던 시간(µs)을 잰다. 6000 µs 안에 안 돌아오면 음수
    if pulse_time < 0:           # 반사가 돌아오지 않았다 = 앞이 비었다 = 아주 멀다
        return 999
    distance_cm = (pulse_time / 2) / 29.1       # 왕복 시간의 절반 ÷ 29.1 = 거리(cm)
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
    buzzer.freq(BEEP_FREQ)                      # freq() 메서드 : 소리 높이(Hz)를 바꾼다
    buzzer.duty(duty)                           # duty() 메서드 : 소리 크기를 정한다 (켜짐)
    time.sleep_ms(BEEP_MS)                      # sleep_ms() : 괄호 안 ms 동안 코드를 멈춘다 (1000 ms = 1초)
    buzzer.duty(0)                              # duty(0) : 소리를 끈다
    time.sleep_ms(REST_MS)                      # sleep_ms() : 괄호 안 ms 동안 코드를 멈춘다 (1000 ms = 1초)

def warning():                   # 삐~ : 길게 울린 뒤 잠깐 끈다 (끈 직후에 거리를 재야 부저가 센서를 흔들지 않는다)
    buzzer.freq(WARN_FREQ)                      # freq() 메서드 : 소리 높이(Hz)를 바꾼다
    buzzer.duty(WARN_DUTY)                      # duty() 메서드 : 소리 크기를 정한다 (켜짐)
    time.sleep_ms(WARN_MS)                      # sleep_ms() : 괄호 안 ms 동안 코드를 멈춘다 (1000 ms = 1초)
    buzzer.duty(0)                              # duty(0) : 소리를 끈다
    time.sleep_ms(MUTE_MS)                      # sleep_ms() : 괄호 안 ms 동안 코드를 멈춘다 (1000 ms = 1초)

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
except KeyboardInterrupt:                       # 정지 버튼(Ctrl + C)을 누르면 여기로 온다
    pass
finally:                                        # 끝날 때 꼭 실행된다 : 부저와 타이머를 정리한다
    buzzer.duty(0)                              # duty(0) : 소리를 끈다
    buzzer.deinit()                             # deinit() 메서드 : 부저를 놓아 준다 (끝낼 때)
