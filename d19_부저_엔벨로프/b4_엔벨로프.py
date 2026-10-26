from machine import Pin, PWM
import time

buzzer = PWM(Pin(6), freq=440, duty=0)

TICK_MS = 10               # 10 ms 마다 소리 크기를 새로 정한다

def envelope_duty(t, total, peak, a, d, s, r):
    # t 시점(ms)의 소리 크기를 돌려준다
    # total : 음 전체 길이   peak : 가장 큰 크기   s : 버티는 크기 (peak 의 몇 %)
    # a 어택(커지는 시간) d 디케이(줄어드는 시간) r 릴리즈(끝에서 사라지는 시간)
    sus = peak * s // 100
    if t < a:                                  # 1) 어택 : 0 -> peak
        return peak * t // a
    if t < a + d:                              # 2) 디케이 : peak -> sus
        return peak - (peak - sus) * (t - a) // d
    if t < total - r:                          # 3) 서스테인 : sus 유지
        return sus
    return sus * (total - t) // r              # 4) 릴리즈 : sus -> 0

def play_note(freq, total, peak, a, d, s, r):
    buzzer.freq(freq)
    t = 0
    while t < total:
        buzzer.duty(envelope_duty(t, total, peak, a, d, s, r))
        time.sleep_ms(TICK_MS)
        t += TICK_MS
    buzzer.duty(0)

# 소리 모양 4가지 : (어택, 디케이, 서스테인 %, 릴리즈)  단위는 ms, 서스테인만 %
SHAPES = {
    "피아노": (10, 300, 20, 200),
    "오르간": (60, 0, 100, 120),
    "종":     (5, 600, 0, 100),
    "바이올린": (250, 100, 70, 250),
}

PEAK = 96                  # 가장 큰 크기 (볼륨 6 쯤)
NOTE_MS = 1500             # 한 음의 길이

try:
    for name, (a, d, s, r) in SHAPES.items():
        print(name, "어택", a, "디케이", d, "서스테인", s, "% 릴리즈", r)
        play_note(440, NOTE_MS, PEAK, a, d, s, r)
        time.sleep_ms(700)
finally:
    buzzer.duty(0)
    buzzer.deinit()
    print("끝")
