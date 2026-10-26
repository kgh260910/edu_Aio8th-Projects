from machine import Pin, PWM
import time

buzzer = PWM(Pin(6), freq=440, duty=0)

TICK_MS = 10
ONE_BEAT_MS = 400          # 한 박 = 400 ms
PEAK = 96                  # 가장 큰 크기 (볼륨 6 쯤)

# 소리 모양 고르기 (어택+디케이+릴리즈 는 한 박 400 ms 를 넘지 않게) : "피아노" "오르간" "종" "바이올린" 중 하나로 바꿔 본다
SHAPE = "피아노"
SHAPES = {
    "피아노": (10, 200, 20, 120),
    "오르간": (40, 0, 100, 80),
    "종":     (5, 300, 0, 80),
    "바이올린": (120, 80, 70, 120),
}

DO, RE, MI, SOL, RA, REST = 523, 587, 659, 784, 880, 0

# [주파수, 박자, 음이름]  박자 1 = 한 박, 2 = 두 박
school_bell = [
    [SOL, 1, "솔"], [SOL, 1, "솔"], [RA, 1, "라"], [RA, 1, "라"],
    [SOL, 1, "솔"], [SOL, 1, "솔"], [MI, 2, "미~"],        # 학교종이 땡땡땡
    [SOL, 1, "솔"], [SOL, 1, "솔"], [MI, 1, "미"], [MI, 1, "미"],
    [RE, 2, "레~"], [REST, 2, "쉬고"],                     # 어서 모이자
    [SOL, 1, "솔"], [SOL, 1, "솔"], [RA, 1, "라"], [RA, 1, "라"],
    [SOL, 1, "솔"], [SOL, 1, "솔"], [MI, 2, "미~"],        # 선생님이 우리를
    [SOL, 1, "솔"], [MI, 1, "미"], [RE, 1, "레"], [MI, 1, "미"],
    [DO, 2, "도~"], [REST, 2, "쉬고"],                     # 기다리신다
]

def envelope_duty(t, total, peak, a, d, s, r):
    sus = peak * s // 100
    if t < a:
        return peak * t // a
    if t < a + d:
        return peak - (peak - sus) * (t - a) // d
    if t < total - r:
        return sus
    return sus * (total - t) // r

def play_note(freq, total, peak, a, d, s, r):
    buzzer.freq(freq)
    t = 0
    while t < total:
        buzzer.duty(envelope_duty(t, total, peak, a, d, s, r))
        time.sleep_ms(TICK_MS)
        t += TICK_MS
    buzzer.duty(0)

try:
    a, d, s, r = SHAPES[SHAPE]
    print("학교종이 땡땡땡 -", SHAPE)
    for freq, beats, name in school_bell:
        total = beats * ONE_BEAT_MS
        print(name, freq, "Hz", beats, "박")
        if freq == REST:
            buzzer.duty(0)
            time.sleep_ms(total)
        else:
            play_note(freq, total, PEAK, a, d, s, r)
    print("연주 끝")
finally:
    buzzer.duty(0)
    buzzer.deinit()
