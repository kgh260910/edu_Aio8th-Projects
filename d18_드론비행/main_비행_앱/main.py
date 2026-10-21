# main_비행_앱 — 새 파이드론 조종기 앱용 코드. main_비행(교재 3-3)에 '배터리 전압을 폰으로 알려 주기' 한 가지를 더했다.
# 이 폴더의 main.py 를 보드에 올린다. 프로펠러를 단 채일 때는 강사가 "됐다"고 하기 전에 배터리를 꽂지 않는다.
import bluetooth, ble_simple_peripheral, time
from machine import Pin, ADC, SoftI2C
from ssd1306 import SSD1306_I2C
import drone

NAME = 'pyD_01'   # ← 내 번호로 바꾼다. 영문·숫자 8글자 이하

ble = bluetooth.BLE()
p = ble_simple_peripheral.BLESimplePeripheral(ble, name=NAME)

d = drone.DRONE(flightmode=1, debug=0)

adc = ADC(Pin(2))                       # 배터리 전압을 읽는 핀 (교재 2-3, f5_OLED_상태.py 와 같다)

oled = SSD1306_I2C(128, 64, SoftI2C(sda=Pin(43), scl=Pin(44)))   # 작은 화면(OLED), f5_OLED_상태.py 와 같다
SHOW_NAME = NAME if all(ord(c) < 128 for c in NAME) else 'DRONE'  # 작은 화면 글꼴은 영문·숫자만 그린다

def read_voltage():
    return adc.read() / 4095 * 5.02 * 0.96     # 교재 2-3 의 환산식

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
    control_data = [None] * 4
    for i in range(4):
        control_data[i] = read[i + 1] - 100

    d.control(rol=control_data[0], pit=control_data[1], yaw=control_data[2], thr=control_data[3])

    if read[5] == 136:
        print('stop')
        d.stop()
    elif read[5] == 24:
        print('take_off')
        d.take_off(distance=120)
    elif read[5] == 72:
        print('landing')
        d.landing()
    elif read[5] == 40:
        print('calibration')
        do_calibration()
    elif read[5] == 1:
        print('button1')
    elif read[5] == 2:
        print('button2')
    elif read[5] == 3:
        print('button3')
    elif read[5] == 4:
        print('button4')

do_calibration()
p.on_write(on_rx)

while True:                              # 1초마다 배터리 전압을 폰에 알리고(예: V3.92), 작은 화면에도 보여 준다
    volt = read_voltage()
    if p.is_connected():
        p.send("V%.2f" % volt)
    oled.fill(0)
    oled.text(SHOW_NAME, 0, 0)
    oled.text("phone: " + ("ON" if p.is_connected() else "wait"), 0, 20)
    oled.text("batt: %.2f V" % volt, 0, 36)
    oled.show()
    time.sleep_ms(1000)
