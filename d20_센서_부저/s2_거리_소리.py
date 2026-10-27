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

# ---- 내가 바꾸는 값 : r2_거리_범위재기.py 로 잰 내 값을 넣는다 ----
NEAR_CM = 5                      # 손을 가장 가까이 둘 때의 거리 (가장 큰 소리)
FAR_CM = 40                      # 손을 가장 멀리 둘 때의 거리 (가장 작은 소리) : NEAR_CM 보다 커야 한다
LEVELS = 20                      # 소리 크기를 몇 단계로 나눌까
# 단계 0~19 -> duty : 약 1 % (10) 에서 약 15 % (150) 까지, 앞쪽은 촘촘하고 뒤쪽은 성기게
DUTY_TABLE = [10, 12, 13, 15, 18, 20, 24, 27, 31, 36, 42, 48, 55, 64, 73, 85, 98, 113, 130, 150]
BEEP_MS = 500
REST_MS = 500

def get_distance_cm():           # 교재 5-3 _2 와 같은 함수 : 못 읽으면 0
    trigger.value(0)                            # value(0) : 끈 상태에서 시작
    time.sleep_us(5)                            # sleep_us() : 5 µs 기다린다 (µs = 마이크로초 = 100만분의 1초)
    trigger.value(1)                            # value(1) : 켠다 = 초음파를 쏘기 시작
    time.sleep_us(10)                           # 10 µs 동안 켜 둔다
    trigger.value(0)                            # value(0) : 끈다 = 쏘기를 끝낸다
    pulse_time = machine.time_pulse_us(echo, 1, 30000)  # time_pulse_us(핀, 1, 최대µs) : echo 가 켜져 있던 시간(µs)을 잰다. 30000 µs 안에 안 돌아오면 음수
    distance_cm = (pulse_time / 2) / 29.1       # 왕복 시간의 절반 ÷ 29.1 = 거리(cm)
    if 2 <= distance_cm <= 200:
        return distance_cm
    else:
        return 0

def distance_level(cm):
    # 가까울수록 큰 단계 : NEAR_CM 이하 -> 19, FAR_CM 이상 -> 0
    level = int((FAR_CM - cm) * LEVELS // (FAR_CM - NEAR_CM))
    if level < 0:
        level = 0
    if level > LEVELS - 1:
        level = LEVELS - 1
    return level

def beep(duty):
    buzzer.duty(duty)                           # duty() 메서드 : 소리 크기를 정한다 (켜짐)
    time.sleep_ms(BEEP_MS)                      # sleep_ms() : 괄호 안 ms 동안 코드를 멈춘다 (1000 ms = 1초)
    buzzer.duty(0)                              # duty(0) : 소리를 끈다
    time.sleep_ms(REST_MS)                      # sleep_ms() : 괄호 안 ms 동안 코드를 멈춘다 (1000 ms = 1초)

level = 9                        # 처음 단계 (못 읽어도 소리 나게)

try:
    while True:
        cm = get_distance_cm()
        if cm != 0:                              # 0 은 못 읽은 것 : 이전 단계를 그대로 쓴다
            level = distance_level(cm)
        duty = DUTY_TABLE[level]
        print("거리", int(cm), "cm -> 단계", level, "-> duty", duty)
        beep(duty)
except KeyboardInterrupt:                       # 정지 버튼(Ctrl + C)을 누르면 여기로 온다
    pass
finally:                                        # 끝날 때 꼭 실행된다 : 부저와 타이머를 정리한다
    buzzer.duty(0)                              # duty(0) : 소리를 끈다
    buzzer.deinit()                             # deinit() 메서드 : 부저를 놓아 준다 (끝낼 때)
