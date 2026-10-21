# route_자동경로 — KEY 버튼을 누르면: 3초 대기 → 이륙 → 앞으로 → 뒤로 → 착륙 (교재 3-4_3 을 읽기 좋게 고침)
# 이 폴더의 main.py 를 보드에 올린다. 폰 앱의 [멈춤] 은 보정 중·비행 중·끝난 뒤 언제든 받는다.
import bluetooth, ble_simple_peripheral, time
from machine import Pin
import drone

NAME = 'pyD_01'   # ← 내 번호로 바꾼다. 8글자 이하. 폰 앱의 [멈춤]을 받으려고 블루투스를 켠다.

ble = bluetooth.BLE()
p = ble_simple_peripheral.BLESimplePeripheral(ble, name=NAME)
d = drone.DRONE(flightmode=1, debug=0)

TRIM_ROL = 0      # 한쪽으로 쏠리면 5~10 부터 조금씩 바꿔 본다 (교재 142쪽: 10~30 정도로 시험)
TRIM_PIT = 0
FRONT = 40        # 앞으로 가는 세기 (pit)
BACK = -40        # 뒤로 가는 세기 (pit)
USE_LANDING = False  # False: 교재처럼 control 만 보낸다(기본) / True: 착륙 구간에서 d.landing() 도 부른다 (강사가 시험해 정해 준다)

key = Pin(0, Pin.IN, Pin.PULL_UP)
prev_key = key.value()
stop_flag = False          # 폰에서 [멈춤] 신호가 오면 True

class EmergencyStop(Exception):
    pass

def on_rx(read):
    global stop_flag
    if len(read) > 5 and read[5] == 136:   # 5번 칸 136 = [멈춤]
        stop_flag = True

p.on_write(on_rx)

def do_calibration():
    green_led = Pin(42, Pin.OUT)
    while True:
        if stop_flag:                  # 보정하는 동안에도 [멈춤] 을 받는다
            raise EmergencyStop()
        if d.read_calibrated():
            green_led.off()
            break
        green_led.on()
        time.sleep_ms(50)
        green_led.off()
        time.sleep_ms(50)

def get_key():
    global prev_key
    curr_key = key.value()
    if curr_key != prev_key:
        prev_key = curr_key
        if curr_key == 0:
            return True
        time.sleep(0.1)
    return False

def phase(name, sec, rol, pit, takeoff=False, land=False):
    print(name, sec, "초")
    for i in range(sec * 20):          # 50ms 마다 한 번씩 명령 (1초에 20번)
        if stop_flag:                  # 폰에서 [멈춤] 이 왔다
            raise EmergencyStop()
        d.control(rol=rol, pit=pit, yaw=0, thr=0)
        if takeoff:
            d.take_off(distance=120)
        if land and USE_LANDING:
            d.landing()
        time.sleep_ms(50)

try:
    do_calibration()
    print("보정 끝 — KEY 를 누르면 시작")
    while True:
        if stop_flag:                  # 경로가 끝난 뒤 기다리는 동안에도 [멈춤] 을 받는다
            raise EmergencyStop()
        if get_key():
            phase("대기", 3, 0, 0)
            phase("이륙", 5, TRIM_ROL, TRIM_PIT, takeoff=True)
            phase("앞으로", 3, TRIM_ROL, FRONT, takeoff=True)
            phase("뒤로", 3, TRIM_ROL, BACK, takeoff=True)
            phase("착륙", 5, TRIM_ROL, TRIM_PIT, land=True)
            print("끝 — 다시 하려면 KEY")
except EmergencyStop:
    d.stop()                           # 날개를 멈춘다
    print("긴급 정지 — 다시 하려면 RST")
except KeyboardInterrupt:
    print("코드를 종료합니다.")
