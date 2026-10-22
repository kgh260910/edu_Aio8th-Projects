# f6 main.py — 보정 값은 끝나면 멈추고, 기울기는 움직이면 변하는 것을 OLED 로 본다
import time
from machine import Pin, SoftI2C
from ssd1306 import SSD1306_I2C
import drone
oled = SSD1306_I2C(128, 64, SoftI2C(sda=Pin(43), scl=Pin(44)))
d = drone.DRONE(flightmode=1, debug=0)
while not d.read_calibrated():       # 보정이 끝날 때까지 (보정 중에는 값이 변한다)
    oled.fill(0)
    oled.text("calibrating...", 0, 0)
    oled.text("%d %d %d" % d.read_cal_data(), 0, 10)
    oled.show()
    time.sleep_ms(100)
cal = d.read_cal_data()              # 끝난 값은 한 번만 읽는다
while True:
    s = d.read_states()              # 앞 세 칸 = roll, pitch, yaw 각도 x100
    oled.fill(0)
    oled.text("cal: no change", 0, 0)
    oled.text("%d %d %d" % cal, 0, 10)
    oled.text("roll  %6.1f" % (s[0] / 100), 0, 32)
    oled.text("pitch %6.1f" % (s[1] / 100), 0, 44)
    oled.show()
    time.sleep_ms(100)
