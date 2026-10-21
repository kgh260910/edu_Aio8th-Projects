# main_비행_끊김안전 — main_비행 에 "폰 신호가 끊기면 스스로 착륙" 한 가지를 더한 코드. 이 폴더의 main.py 를 보드에 올린다.
# 교재 코드는 연결이 끊겨도 마지막 명령을 계속 따를 수 있다. 이 코드는 0.5초 동안 신호가 없으면 착륙한다.
# (앱은 값을 50ms 마다 보낸다 — 교재 3-1 실행 결과)  ※ 강사가 프로펠러 없이 먼저 확인한 뒤 사용한다.
import bluetooth, ble_simple_peripheral, time
from machine import Pin
import drone

NAME = 'pyD_01'        # ← 내 번호로 바꾼다. 8글자 이하
LOST_MS = 500          # 이 시간(ms) 동안 신호가 없으면 착륙

ble = bluetooth.BLE()
p = ble_simple_peripheral.BLESimplePeripheral(ble, name=NAME)
d = drone.DRONE(flightmode=1, debug=0)

last_rx = time.ticks_ms()   # 마지막으로 신호를 받은 시각
in_air = False              # 이륙 명령을 받은 뒤 True

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

def on_rx(read):
    global last_rx, in_air
    last_rx = time.ticks_ms()
    control_data = [None] * 4
    for i in range(4):
        control_data[i] = read[i + 1] - 100

    d.control(rol=control_data[0], pit=control_data[1], yaw=control_data[2], thr=control_data[3])

    if read[5] == 136:
        print('stop')
        in_air = False
        d.stop()
    elif read[5] == 24:
        print('take_off')
        in_air = True
        d.take_off(distance=120)
    elif read[5] == 72:
        print('landing')
        in_air = False
        d.landing()
    elif read[5] == 40:
        print('calibration')
        do_calibration()

do_calibration()
p.on_write(on_rx)

while True:
    if in_air and time.ticks_diff(time.ticks_ms(), last_rx) > LOST_MS:
        print('신호 끊김 -> landing')
        in_air = False
        d.landing()
    time.sleep_ms(100)
