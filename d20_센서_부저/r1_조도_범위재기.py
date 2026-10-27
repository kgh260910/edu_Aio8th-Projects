from machine import Pin, ADC                    # machine 에서 부품 도구(클래스)를 가져온다 : Pin(핀), ADC(조도센서 읽기)
import time                                     # time : 기다리거나 시간을 다루는 도구 모음

# 조도센서 객체 만들기 : ADC 클래스(숫자로 읽는 설계도)로 cds_sensor 를 만든다. Pin(8) = 8번 핀(보드 표기 IO8)
cds_sensor = ADC(Pin(8))
cds_sensor.atten(ADC.ATTN_11DB)                 # atten() 메서드 : 읽는 전압 범위를 가장 넓게(11 dB) 맞춘다 -> 값이 0~4095

lo = 4095                        # 지금까지 본 가장 작은 값 (가장 어두울 때) : 처음에는 아주 큰 값에서 시작한다
hi = 0                           # 지금까지 본 가장 큰 값 (가장 밝을 때) : 처음에는 아주 작은 값에서 시작한다

try:
    while True:
        value = cds_sensor.read()               # read() 메서드 : 밝기를 숫자(0~4095)로 읽는다
        if value < lo:           # 지금까지 본 것보다 더 작으면 최소를 바꾼다
            lo = value
        if value > hi:           # 지금까지 본 것보다 더 크면 최대를 바꾼다
            hi = value
        print("지금", value, "| 최소", lo, "| 최대", hi)
        time.sleep(0.2)                         # sleep() : 괄호 안 초 동안 코드를 멈춘다
except KeyboardInterrupt:                       # 정지 버튼(Ctrl + C)을 누르면 여기로 온다
    print("내 조도 범위 : 최소", lo, "최대", hi)
