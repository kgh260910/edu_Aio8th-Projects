from machine import Pin, PWM
import time

buzzer = PWM(Pin(6), freq=440, duty=0)

# 볼륨 0 ~ 10 단계를 duty 숫자로 바꾸는 표 (b1 에서 들어 본 결과로 고른 값)
# 앞쪽은 촘촘하고 뒤쪽은 성기다 : 귀는 작은 소리의 차이를 더 잘 느낀다
VOLUME_TABLE = [0, 3, 6, 12, 24, 48, 96, 160, 256, 384, 512]
MAX_LEVEL = len(VOLUME_TABLE) - 1            # 10

volume = 3                                   # 지금 볼륨 (0 ~ 10), 작게 시작

def set_volume(level):
    global volume
    volume = max(0, min(MAX_LEVEL, level))   # 0 ~ 10 밖의 숫자는 끝값으로 맞춘다
    return VOLUME_TABLE[volume]

def tone(freq, ms):
    buzzer.freq(freq)
    buzzer.duty(VOLUME_TABLE[volume])
    time.sleep_ms(ms)
    buzzer.duty(0)
    time.sleep_ms(80)                        # 소리 사이 짧은 쉼

try:
    print("볼륨 1 ~ 10 을 차례로 같은 음(라 440 Hz)으로 듣는다")
    for level in range(1, MAX_LEVEL + 1):
        duty = set_volume(level)
        print("볼륨", level, "-> duty", duty)
        tone(440, 500)

    print("볼륨 3 으로 돌아와 도레미를 낸다")
    set_volume(3)
    for freq in (523, 587, 659):
        tone(freq, 400)
finally:
    buzzer.duty(0)
    buzzer.deinit()
    print("끝")
