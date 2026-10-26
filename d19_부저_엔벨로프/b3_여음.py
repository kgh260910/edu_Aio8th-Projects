from machine import Pin, PWM
import time

buzzer = PWM(Pin(6), freq=440, duty=0)

PEAK = 96                  # 음이 시작할 때의 소리 크기 (볼륨 6 쯤)
MIN_DUTY = 8               # 여음이 사라지기 직전의 소리 크기
FADE_STEPS = 12            # 줄이는 단계 수 (많을수록 부드럽다)

def play_flat(freq, ms):
    # 크기가 처음부터 끝까지 같다 : 끝에서 뚝 끊긴다
    buzzer.freq(freq)
    buzzer.duty(PEAK)
    time.sleep_ms(ms)
    buzzer.duty(0)

def play_decay(freq, ms):
    # 크기를 PEAK 에서 MIN_DUTY 까지 조금씩 줄인다 : 소리가 잦아든다
    buzzer.freq(freq)
    step_ms = ms // FADE_STEPS
    for i in range(FADE_STEPS):
        duty = PEAK - (PEAK - MIN_DUTY) * i // (FADE_STEPS - 1)
        buzzer.duty(duty)
        time.sleep_ms(step_ms)
    buzzer.duty(0)

try:
    print("1) 평평한 소리 - 라(440 Hz) 1.2초")
    play_flat(440, 1200)
    time.sleep_ms(800)

    print("2) 잦아드는 소리 - 같은 음, 같은 길이")
    play_decay(440, 1200)
    time.sleep_ms(800)

    print("3) 도 레 미 파 솔 : 평평 -> 잦아듦 차례로")
    for freq in (523, 587, 659, 698, 784):
        play_flat(freq, 400)
        time.sleep_ms(150)
    time.sleep_ms(600)
    for freq in (523, 587, 659, 698, 784):
        play_decay(freq, 400)
        time.sleep_ms(150)
finally:
    buzzer.duty(0)
    buzzer.deinit()
    print("끝")
