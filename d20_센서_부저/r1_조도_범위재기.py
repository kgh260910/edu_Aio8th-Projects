from machine import Pin, ADC
import time

cds_sensor = ADC(Pin(8))
cds_sensor.atten(ADC.ATTN_11DB)

lo = 4095                        # 지금까지 본 가장 작은 값 (가장 어두울 때) : 처음에는 아주 큰 값에서 시작한다
hi = 0                           # 지금까지 본 가장 큰 값 (가장 밝을 때) : 처음에는 아주 작은 값에서 시작한다

try:
    while True:
        value = cds_sensor.read()
        if value < lo:           # 지금까지 본 것보다 더 작으면 최소를 바꾼다
            lo = value
        if value > hi:           # 지금까지 본 것보다 더 크면 최대를 바꾼다
            hi = value
        print("지금", value, "| 최소", lo, "| 최대", hi)
        time.sleep(0.2)
except KeyboardInterrupt:
    print("내 조도 범위 : 최소", lo, "최대", hi)
