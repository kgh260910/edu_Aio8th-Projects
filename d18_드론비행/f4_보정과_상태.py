# f4 — 켠 직후 보정이 끝나는지 본다. 모터는 돌리지 않는다
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
