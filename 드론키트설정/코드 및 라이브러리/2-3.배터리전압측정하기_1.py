from machine import Pin,ADC
import time

adc = ADC(Pin(2))

try:
    while True:
        adc_value = adc.read()
        
        print(adc_value)

        time.sleep(1.0)

except KeyboardInterrupt:
    print("코드를 종료합니다.")