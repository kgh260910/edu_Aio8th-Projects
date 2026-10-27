from machine import Pin, PWM, ADC               # machine 에서 부품 도구(클래스)를 가져온다 : Pin(핀), PWM(부저), ADC(조도센서 읽기)
import time                                     # time : 기다리거나 시간을 다루는 도구 모음

# 부저 객체 만들기 : PWM 클래스(설계도)로 buzzer 를 만든다
#   Pin(6) = 6번 핀에 달린 부저, freq=880 = 소리 높이 880 Hz, duty=0 = 처음에는 소리 끔 (0~1023)
buzzer = PWM(Pin(6), freq=880, duty=0)
# 조도센서 객체 만들기 : ADC 클래스(숫자로 읽는 설계도)로 cds_sensor 를 만든다. Pin(8) = 8번 핀(보드 표기 IO8)
cds_sensor = ADC(Pin(8))
cds_sensor.atten(ADC.ATTN_11DB)                 # atten() 메서드 : 읽는 전압 범위를 가장 넓게(11 dB) 맞춘다 -> 값이 0~4095

# ---- 내가 바꾸는 값 : r1_조도_범위재기.py 로 잰 내 값을 넣는다 ----
LIGHT_MIN = 340                  # 가장 어두울 때의 값 (교재 예시)
LIGHT_MAX = 865                  # 가장 밝을 때의 값 (교재 예시) : LIGHT_MIN 보다 커야 한다
LEVELS = 20                      # 소리 크기를 몇 단계로 나눌까
# 단계 0~19 -> duty : 약 1 % (10) 에서 약 15 % (150) 까지, 앞쪽은 촘촘하고 뒤쪽은 성기게
DUTY_TABLE = [10, 12, 13, 15, 18, 20, 24, 27, 31, 36, 42, 48, 55, 64, 73, 85, 98, 113, 130, 150]
BEEP_MS = 500                    # 삑 울리는 시간
REST_MS = 500                    # 쉬는 시간

def light_level(value):
    # LIGHT_MIN ~ LIGHT_MAX 사이를 20 칸으로 나눠 몇 번째 칸인지 구한다 (0~19 : 리스트 번호와 같다)
    level = (value - LIGHT_MIN) * LEVELS // (LIGHT_MAX - LIGHT_MIN)
    if level < 0:
        level = 0
    if level > LEVELS - 1:
        level = LEVELS - 1
    return level

def beep(duty):
    buzzer.duty(duty)            # 켜 두고 BEEP_MS 만큼 기다린다
    time.sleep_ms(BEEP_MS)                      # sleep_ms() : 괄호 안 ms 동안 코드를 멈춘다 (1000 ms = 1초)
    buzzer.duty(0)                              # duty(0) : 소리를 끈다
    time.sleep_ms(REST_MS)       # 쉬는 동안에도 코드는 여기서 멈춰 있다


try:
    while True:
        value = cds_sensor.read()               # read() 메서드 : 밝기를 숫자(0~4095)로 읽는다
        level = light_level(value)
        duty = DUTY_TABLE[level]
        print("조도", value, "-> 단계", level, "-> duty", duty)
        beep(duty)
except KeyboardInterrupt:                       # 정지 버튼(Ctrl + C)을 누르면 여기로 온다
    pass
finally:                                        # 끝날 때 꼭 실행된다 : 부저와 타이머를 정리한다
    buzzer.duty(0)                              # duty(0) : 소리를 끈다
    buzzer.deinit()                             # deinit() 메서드 : 부저를 놓아 준다 (끝낼 때)
