from machine import Pin
import time
from machine import SoftI2C
from ssd1306 import SSD1306_I2C

i2c = SoftI2C(sda=Pin(43), scl=Pin(44))
oled = SSD1306_I2C(128, 64, i2c)

oled.fill(0) 
oled.hline(0, 32, 127, 1) 
oled.vline(63, 0, 63, 1)
oled.line(0, 0, 127, 63, 1) 
oled.rect(10, 10, 107, 43, 1)
oled.fill_rect(20, 20, 30, 30, 1)
oled.show()