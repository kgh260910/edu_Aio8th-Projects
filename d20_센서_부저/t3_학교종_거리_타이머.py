import machine                                  # machine : 보드의 부품(핀·타이머 등)을 다루는 도구 모음
import time                                     # time : 기다리거나 시간을 다루는 도구 모음
from machine import Pin, PWM, Timer             # machine 에서 부품 도구(클래스)를 가져온다 : Pin(핀), PWM(부저), Timer(타이머)

# 부저 객체 만들기 : PWM 클래스(설계도)로 buzzer 를 만든다
#   Pin(6) = 6번 핀에 달린 부저, freq=440 = 소리 높이 440 Hz, duty=0 = 처음에는 소리 끔 (0~1023)
buzzer = PWM(Pin(6), freq=440, duty=0)
# trigger 객체 만들기 : Pin 클래스로 17번 핀을 쓴다. mode=Pin.OUT = 내보내는 핀(소리를 쏘라는 신호), pull=None = 내부 저항은 안 쓴다
trigger = Pin(17, mode=Pin.OUT, pull=None)
# echo 객체 만들기 : 1번 핀. mode=Pin.IN = 받는 핀(돌아온 소리 신호), pull=None = 내부 저항은 안 쓴다
echo = Pin(1, mode=Pin.IN, pull=None)
trigger.value(0)                                # value() 메서드 : 핀 값을 정한다. 0 = 끔 (처음에는 소리를 쏘지 않는다)

# ---- 내가 바꾸는 값 ----
NEAR_CM = 5                      # 손을 가장 가까이 둘 때의 거리 (가장 작은 소리)
FAR_CM = 60                      # 손을 가장 멀리 둘 때의 거리 (가장 큰 소리) : NEAR_CM 보다 커야 한다
LEVELS = 20                      # 소리 크기를 몇 단계로 나눌까
DUTY_TABLE = [10, 12, 13, 15, 18, 20, 24, 27, 31, 36, 42, 48, 55, 64, 73, 85, 98, 113, 130, 150]
EIGHTH_MS = 200                  # 8분음표 한 개의 길이 : 4분음표 = 2개 = 400 ms
GAP_MS = 100                     # 음이 끝나기 전에 부저를 꺼 두는 시간 : 땡-땡이 끊겨 들리고, 이 틈에 거리를 잰다
LISTEN_MS = 60                   # 부저를 끈 뒤 이만큼 기다렸다가 잰다 (소리가 나는 중에 재면 부저가 센서를 흔든다)

# 계명 -> 주파수(Hz). 쉼은 0
NOTE_HZ = {"도": 523, "레": 587, "미": 659, "솔": 784, "라": 880, "쉼": 0}

# (계명, 음길이)  음길이 : 8분음표 몇 개 만큼 자리를 차지하나 (1 = 8분, 2 = 4분, 4 = 2분)
school_bell = [
    ("솔", 2), ("솔", 2), ("라", 2), ("라", 2),
    ("솔", 2), ("솔", 2), ("미", 4),                  # 학교종이 땡땡땡
    ("솔", 2), ("솔", 2), ("미", 2), ("미", 2),
    ("레", 4), ("쉼", 4),                             # 어서 모이자
    ("솔", 2), ("솔", 2), ("라", 2), ("라", 2),
    ("솔", 2), ("솔", 2), ("미", 4),                  # 선생님이 우리를
    ("솔", 2), ("미", 2), ("레", 2), ("미", 2),
    ("도", 4), ("쉼", 4),                             # 기다리신다
]

# ---- 인터럽트 깃발 : 알람 ----
ms = 0
flag_10 = False
flag_500 = False

def tick(t):
    global ms, flag_10, flag_500                # global : 이 함수 안에서 바깥 변수의 값을 바꾼다고 알린다
    ms += 1
    if ms % 10 == 0:
        flag_10 = True
    if ms % 500 == 0:
        flag_500 = True

def get_distance_cm():           # 교재 5-3 _2 와 같은 함수 : 못 읽으면 0
    trigger.value(0)                            # value(0) : 끈 상태에서 시작
    time.sleep_us(5)                            # sleep_us() : 5 µs 기다린다 (µs = 마이크로초 = 100만분의 1초)
    trigger.value(1)                            # value(1) : 켠다 = 초음파를 쏘기 시작
    time.sleep_us(10)                           # 10 µs 동안 켜 둔다
    trigger.value(0)                            # value(0) : 끈다 = 쏘기를 끝낸다
    # 6000 µs (약 100 cm) 까지만 기다린다 : 오래 기다리면 그동안 타이머 틱을 놓친다 (교재는 30000)
    pulse_time = machine.time_pulse_us(echo, 1, 6000)  # time_pulse_us(핀, 1, 최대µs) : echo 가 켜져 있던 시간(µs)을 잰다. 6000 µs 안에 안 돌아오면 음수
    distance_cm = (pulse_time / 2) / 29.1       # 왕복 시간의 절반 ÷ 29.1 = 거리(cm)
    if 2 <= distance_cm <= 200:
        return distance_cm
    else:
        return 0

def distance_level(cm):
    # 가까울수록 작은 단계 (t2 와 반대) : NEAR_CM 이하 -> 0, FAR_CM 이상 -> 19
    level = int((cm - NEAR_CM) * LEVELS // (FAR_CM - NEAR_CM))
    if level < 0:
        level = 0
    if level > LEVELS - 1:
        level = LEVELS - 1
    return level

idx = 0                          # 지금 몇 번째 음인가
note_start = 0                   # 이 음이 시작한 ms
measured = False                 # 이 음에서 거리를 이미 쟀는가
cm = 0
level = 9
duty = DUTY_TABLE[level]
buzzer.freq(NOTE_HZ[school_bell[0][0]])         # freq() 메서드 : 소리 높이(Hz)를 바꾼다

# tmr 객체 만들기 : Timer 클래스로 0번 하드웨어 타이머를 쓴다
tmr = Timer(0)
# init() 메서드로 타이머를 켠다 : period=1 = 1 ms 마다, mode=Timer.PERIODIC = 계속 반복, callback=tick = 때마다 tick 함수를 부른다
tmr.init(period=1, mode=Timer.PERIODIC, callback=tick)

try:
    while True:
        if flag_10:                              # 10 ms : 음을 넘기고, 소리 크기를 주고, 소리를 끈 틈에 거리를 잰다
            flag_10 = False
            name, length = school_bell[idx]
            t = ms - note_start                  # 이 음이 시작하고 지난 ms
            if t >= length * EIGHTH_MS:          # 자리가 끝났다 -> 다음 음으로 (끝까지 가면 처음부터 다시)
                note_start += length * EIGHTH_MS
                idx = idx + 1
                if idx >= len(school_bell):      # 곡이 끝났으면 처음부터 다시
                    idx = 0
                name, length = school_bell[idx]
                t = ms - note_start
                measured = False
                if NOTE_HZ[name] != 0:
                    buzzer.freq(NOTE_HZ[name])  # freq() 메서드 : 소리 높이(Hz)를 바꾼다
            left = length * EIGHTH_MS - t        # 이 음이 끝나기까지 남은 ms
            if name == "쉼" or left <= GAP_MS:   # 쉬는 시간이거나 음이 끝나기 직전이면 소리를 끈다
                buzzer.duty(0)                  # duty(0) : 소리를 끈다
                if not measured and (name == "쉼" or left <= GAP_MS - LISTEN_MS):
                    measured = True              # 소리를 끈 지 60 ms 가 지났다 : 이 음에서 한 번만 잰다
                    cm = get_distance_cm()
                    if cm != 0:                  # 0 은 못 읽은 것 : 이전 단계를 그대로 쓴다
                        level = distance_level(cm)
                        duty = DUTY_TABLE[level]
            else:
                buzzer.duty(duty)               # duty() 메서드 : 소리 크기를 정한다 (켜짐)
        if flag_500:                             # 500 ms : 어디쯤인지 쉘에 찍는다
            flag_500 = False
            print("거리", int(cm), "cm -> 단계", level, "-> duty", duty, "|", idx + 1, "/", len(school_bell), school_bell[idx][0])
except KeyboardInterrupt:                       # 정지 버튼(Ctrl + C)을 누르면 여기로 온다
    pass
finally:                                        # 끝날 때 꼭 실행된다 : 부저와 타이머를 정리한다
    tmr.deinit()                                # deinit() 메서드 : 타이머를 끈다
    buzzer.duty(0)                              # duty(0) : 소리를 끈다
    buzzer.deinit()                             # deinit() 메서드 : 부저를 놓아 준다 (끝낼 때)
