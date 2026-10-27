import machine                                  # machine : 보드의 부품(핀·타이머 등)을 다루는 도구 모음
import time                                     # time : 기다리거나 시간을 다루는 도구 모음
from machine import Pin                         # machine 에서 부품 도구(클래스)를 가져온다 : Pin(핀)

# trigger 객체 만들기 : Pin 클래스로 17번 핀을 쓴다. mode=Pin.OUT = 내보내는 핀(소리를 쏘라는 신호), pull=None = 내부 저항은 안 쓴다
trigger = Pin(17, mode=Pin.OUT, pull=None)
# echo 객체 만들기 : 1번 핀. mode=Pin.IN = 받는 핀(돌아온 소리 신호), pull=None = 내부 저항은 안 쓴다
echo = Pin(1, mode=Pin.IN, pull=None)
trigger.value(0)                                # value() 메서드 : 핀 값을 정한다. 0 = 끔 (처음에는 소리를 쏘지 않는다)

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
        time.sleep(0.2)                         # sleep() : 괄호 안 초 동안 코드를 멈춘다
except KeyboardInterrupt:                       # 정지 버튼(Ctrl + C)을 누르면 여기로 온다
    print("내 거리 범위 : 가장 가까움", int(lo), "가장 멈", int(hi))
