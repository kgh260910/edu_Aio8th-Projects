from machine import Pin
import time
from machine import SoftI2C
from ssd1306 import SSD1306_I2C

i2c = SoftI2C(sda=Pin(43), scl=Pin(44))
oled = SSD1306_I2C(128, 64, i2c)

cnt = 0
try:
    while True:
        oled.fill(0) 
        oled.text(str(cnt),50,20)
        oled.show()
        
        cnt += 1
        time.sleep(0.2)
except:
    pass