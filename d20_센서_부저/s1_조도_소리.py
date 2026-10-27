from machine import Pin, PWM, ADC
import time

buzzer = PWM(Pin(6), freq=880, duty=0)
cds_sensor = ADC(Pin(8))
cds_sensor.atten(ADC.ATTN_11DB)

# ---- 내가 바꾸는 값 : r1_조도_범위재기.py 로 잰 내 값을 넣는다 ----
LIGHT_MIN = 340                  # 가장 어두울 때의 값 (교재 예시)
LIGHT_MAX = 865                  # 가장 밝을 때의 값 (교재 예시) : LIGHT_MIN 보다 커야 한다
LEVELS = 20                      # 소리 크기를 몇 단계로 나눌까
# 단계 1~20 -> duty : 약 1 % (10) 에서 50 % (512) 까지, 앞쪽은 촘촘하고 뒤쪽은 성기게
DUTY_TABLE = [10, 12, 15, 19, 23, 28, 35, 43, 52, 65, 79, 98, 120, 148, 182, 224, 275, 338, 416, 512]
BEEP_MS = 500                    # 삑 울리는 시간
REST_MS = 500                    # 쉬는 시간

def light_level(value):
    # LIGHT_MIN ~ LIGHT_MAX 사이를 20 칸으로 나눠 몇 번째 칸인지 구한다 (1~20)
    level = (value - LIGHT_MIN) * LEVELS // (LIGHT_MAX - LIGHT_MIN) + 1
    return max(1, min(LEVELS, level))        # 범위 밖은 끝 칸으로 맞춘다

def beep(duty):
    buzzer.duty(duty)            # 켜 두고 BEEP_MS 만큼 기다린다
    time.sleep_ms(BEEP_MS)
    buzzer.duty(0)
    time.sleep_ms(REST_MS)       # 쉬는 동안에도 코드는 여기서 멈춰 있다

last_look = time.ticks_ms()      # 센서를 마지막으로 본 시각

try:
    while True:
        value = cds_sensor.read()
        level = light_level(value)
        duty = DUTY_TABLE[level - 1]
        now = time.ticks_ms()
        gap = time.ticks_diff(now, last_look)    # 센서를 다시 보기까지 걸린 시간
        last_look = now
        print("조도", value, "-> 단계", level, "-> duty", duty, "| 센서를 다시 보기까지", gap, "ms")
        beep(duty)
except KeyboardInterrupt:
    pass
finally:
    buzzer.duty(0)
    buzzer.deinit()
