from machine import Pin, PWM
import time

buzzer = PWM(Pin(6), freq=440, duty=0)

TICK_MS = 10
VOLUME_TABLE = [0, 3, 6, 12, 24, 48, 96, 160, 256, 384, 512]
VOLUME = 6                                   # 상태음 볼륨 (0 ~ 10)

def envelope_duty(t, total, peak, a, d, s, r):
    sus = peak * s // 100
    if t < a:
        return peak * t // a
    if t < a + d:
        return peak - (peak - sus) * (t - a) // d
    if t < total - r:
        return sus
    return sus * (total - t) // r

def play_note(freq, total, a, d, s, r):
    peak = VOLUME_TABLE[VOLUME]
    buzzer.freq(freq)
    t = 0
    while t < total:
        buzzer.duty(envelope_duty(t, total, peak, a, d, s, r))
        time.sleep_ms(TICK_MS)
        t += TICK_MS
    buzzer.duty(0)

# 소리 신호 하나 = [주파수, 길이 ms] 목록. 주파수 0 은 쉼.
SOUNDS = {
    "켜짐":       [[523, 120], [659, 120], [784, 220]],               # 도 미 솔 : 올라간다
    "준비 끝":    [[784, 100], [0, 60], [784, 100], [1047, 300]],      # 솔 솔 높은도
    "이륙":       [[392, 120], [494, 120], [587, 120], [784, 240]],    # 점점 높아진다
    "착륙":       [[784, 120], [587, 120], [494, 120], [392, 240]],    # 점점 낮아진다
    "배터리 부족": [[880, 150], [0, 100], [880, 150], [0, 100], [880, 150]],  # 같은 음 세 번
    "연결 끊김":   [[330, 700]],                                       # 낮고 긴 소리 하나
}

# 신호마다 소리 모양 (어택, 디케이, 서스테인 %, 릴리즈)
SHAPE_OF = {
    "켜짐": (5, 60, 60, 40),
    "준비 끝": (5, 30, 60, 40),
    "이륙": (5, 40, 80, 40),
    "착륙": (5, 40, 80, 40),
    "배터리 부족": (2, 20, 90, 20),          # 또렷하게 : 빨리 커지고 빨리 끝난다
    "연결 끊김": (20, 200, 30, 250),
}

def play_sound(name):
    a, d, s, r = SHAPE_OF[name]
    for freq, ms in SOUNDS[name]:
        if freq == 0:
            buzzer.duty(0)
            time.sleep_ms(ms)
        else:
            play_note(freq, ms, a, d, s, r)
            time.sleep_ms(20)

try:
    for name in SOUNDS:
        print("소리 신호 :", name)
        play_sound(name)
        time.sleep_ms(1200)
finally:
    buzzer.duty(0)
    buzzer.deinit()
    print("끝")
