# f5_OLED_상태.py — 작은 화면(OLED)에 배터리 전압을 보여 준다. 비행 전 확인용. 모터는 돌리지 않는다.
# 필요: 보드 안에 ssd1306.py
from machine import Pin, SoftI2C, ADC
import time
from ssd1306 import SSD1306_I2C

i2c = SoftI2C(sda=Pin(43), scl=Pin(44))
oled = SSD1306_I2C(128, 64, i2c)

adc = ADC(Pin(2))

while True:
    voltage = adc.read() / 4095 * 5.02 * 0.96     # 교재 2-3 의 환산식
    percent = (voltage - 3.0) / (4.25 - 3.0) * 100
    percent = max(0, min(100, percent))
    oled.fill(0)
    oled.text("battery", 0, 0)
    oled.text("%.2f V" % voltage, 0, 16)
    oled.text("%d %%" % percent, 0, 32)
    oled.text("OK" if percent >= 50 else "CHARGE", 0, 48)
    oled.show()
    time.sleep_ms(500)
