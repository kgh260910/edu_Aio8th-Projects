# f4_보정과_상태.py — 드론 모듈을 켜고 보정(캘리브레이션)이 끝나는지 본다. 모터는 돌리지 않는다.
# 평평한 곳에 놓고 실행한다. 초록 LED(GPIO42)가 깜빡이는 동안 움직이지 않는다.
import time
from machine import Pin
import drone

d = drone.DRONE(flightmode=1, debug=0)

def do_calibration():
    green_led = Pin(42, Pin.OUT)
    while True:
        print(d.read_cal_data())
        if d.read_calibrated():
            print(d.read_cal_data())
            green_led.off()
            break
        green_led.on()
        time.sleep_ms(50)
        green_led.off()
        time.sleep_ms(50)

do_calibration()
print("보정 끝")
