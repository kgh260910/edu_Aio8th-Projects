# f6 — 보정 값은 끝나면 멈추고, 기울기는 움직이면 변하는 것을 OLED 로 본다. 모터는 돌리지 않는다
import time, math, struct
from machine import Pin, SoftI2C
from ssd1306 import SSD1306_I2C
import drone
oled = SSD1306_I2C(128, 64, SoftI2C(sda=Pin(43), scl=Pin(44)))
imu = SoftI2C(sda=Pin(16), scl=Pin(15))   # 기울기 센서 MPU6050 의 선
d = drone.DRONE(flightmode=1, debug=0)
while not d.read_calibrated():            # 보정이 끝날 때까지 기다린다
    time.sleep_ms(100)
cal = d.read_cal_data()                   # 끝난 값은 한 번만 읽는다
while True:
    x, y, z = struct.unpack(">hhh", imu.readfrom_mem(0x68, 0x3B, 6))   # 가속도 x, y, z
    roll = math.degrees(math.atan2(y, z))
    pitch = math.degrees(math.atan2(-x, math.sqrt(y * y + z * z)))
    oled.fill(0)
    oled.text("cal : no change", 0, 0)
    oled.text("%d %d %d" % cal, 0, 10)
    oled.text("tilt: changes", 0, 28)
    oled.text("roll  %6.1f" % roll, 0, 38)
    oled.text("pitch %6.1f" % pitch, 0, 48)
    oled.show()
    time.sleep_ms(100)
