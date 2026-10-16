from machine import Pin,ADC
import time

adc = ADC(Pin(2))

try:
    while True:
        voltage = adc.read()/4095*5.02*0.96
        percent = (voltage - 3.0) / (4.25 - 3.0) * 100
        print(percent)
        time.sleep(1.0)

except KeyboardInterrupt:
    print("코드를 종료합니다.")