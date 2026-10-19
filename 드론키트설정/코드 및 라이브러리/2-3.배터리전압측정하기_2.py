from machine import Pin,ADC
import time

adc = ADC(Pin(2))

try:
    while True:
        voltage = adc.read()/4095*5.02*0.96
        
        print(voltage)

        time.sleep(1.0)

except KeyboardInterrupt:
    print("코드를 종료합니다.")