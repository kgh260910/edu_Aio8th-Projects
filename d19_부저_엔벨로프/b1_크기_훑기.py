from machine import Pin, PWM
import time

buzzer = PWM(Pin(6), freq=440, duty=0)      # 부저는 GPIO 6, 소리 없이 시작

# 소리 높이는 440 Hz 로 고정하고, duty(소리 크기 숫자)만 올렸다가 내린다
UP = [0, 16, 32, 64, 128, 256, 384, 512, 640, 768, 896, 1023]
STEP_MS = 700                                # 숫자 하나당 0.7초 듣는다

try:
    print("올라간다 : 숫자가 커질 때 소리가 어떻게 달라지나 듣는다")
    for duty in UP:
        print("duty", duty)
        buzzer.duty(duty)
        time.sleep_ms(STEP_MS)

    print("내려간다 : 같은 숫자를 거꾸로")
    for duty in reversed(UP):
        print("duty", duty)
        buzzer.duty(duty)
        time.sleep_ms(STEP_MS)
finally:
    buzzer.duty(0)
    buzzer.deinit()
    print("끝")
