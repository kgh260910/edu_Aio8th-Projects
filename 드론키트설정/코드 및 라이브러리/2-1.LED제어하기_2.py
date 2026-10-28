from machine import Pin
import time

green_led = Pin(42,Pin.OUT)

try:
    while True:
        green_led.value(0)
        time.sleep(1.0)
        green_led.value(1)
        time.sleep(1.0)

except KeyboardInterrupt:
    green_led.value(0)
    print("코드를 종료합니다.")