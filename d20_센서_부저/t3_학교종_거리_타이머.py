import machine
import time
from machine import Pin, PWM, Timer

buzzer = PWM(Pin(6), freq=440, duty=0)
trigger = Pin(17, mode=Pin.OUT, pull=None)
echo = Pin(1, mode=Pin.IN, pull=None)
trigger.value(0)

# ---- 내가 바꾸는 값 ----
NEAR_CM = 5                      # 손을 가장 가까이 둘 때의 거리 (가장 작은 소리)
FAR_CM = 60                      # 손을 가장 멀리 둘 때의 거리 (가장 큰 소리) : NEAR_CM 보다 커야 한다
LEVELS = 20                      # 소리 크기를 몇 단계로 나눌까
DUTY_TABLE = [10, 12, 15, 19, 23, 28, 35, 43, 52, 65, 79, 98, 120, 148, 182, 224, 275, 338, 416, 512]
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
    global ms, flag_10, flag_500
    ms += 1
    if ms % 10 == 0:
        flag_10 = True
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
buzzer.freq(NOTE_HZ[school_bell[0][0]])

tmr = Timer(0)
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
                    buzzer.freq(NOTE_HZ[name])
            left = length * EIGHTH_MS - t        # 이 음이 끝나기까지 남은 ms
            if name == "쉼" or left <= GAP_MS:   # 쉬는 시간이거나 음이 끝나기 직전이면 소리를 끈다
                buzzer.duty(0)
                if not measured and (name == "쉼" or left <= GAP_MS - LISTEN_MS):
                    measured = True              # 소리를 끈 지 60 ms 가 지났다 : 이 음에서 한 번만 잰다
                    cm = get_distance_cm()
                    if cm != 0:                  # 0 은 못 읽은 것 : 이전 단계를 그대로 쓴다
                        level = distance_level(cm)
                        duty = DUTY_TABLE[level]
            else:
                buzzer.duty(duty)
        if flag_500:                             # 500 ms : 어디쯤인지 쉘에 찍는다
            flag_500 = False
            print("거리", int(cm), "cm -> 단계", level, "-> duty", duty, "|", idx + 1, "/", len(school_bell), school_bell[idx][0])
except KeyboardInterrupt:
    pass
finally:
    tmr.deinit()
    buzzer.duty(0)
    buzzer.deinit()
