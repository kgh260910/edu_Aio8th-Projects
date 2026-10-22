# f4_보정과_상태/main.py — f4_보정과_상태.py 와 같은 코드. 보드에 main.py 로 올려 두고 RST 로 켜면, 켠 직후 보정이 일어나는 동안 초록 LED(GPIO42)가 깜빡이다 멈춘다.
# 모터는 돌리지 않는다. 평평한 곳에 놓고 RST 를 누른 뒤 손을 뗀다. 3교시 뒤쪽에서 main_비행/main.py 를 올리면 이 파일은 그 코드로 바뀐다.
import time
from machine import Pin
import drone

d = drone.DRONE(flightmode=1, debug=0)

def do_calibration():
    green_led = Pin(42, Pin.OUT)
    if d.read_calibrated():
        print("이미 보정된 보드 (RST 직후에만 LED 깜빡임)")
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
