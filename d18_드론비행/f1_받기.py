# f1_받기.py — 폰 앱이 보낸 값을 그대로 쉘에 찍는다 (교재 3-1_1)
import bluetooth, ble_simple_peripheral, time

NAME = 'pyD_01'   # ← 내 번호로 바꾼다. 영문·숫자 8글자 이하, 교실에서 나만의 이름

ble = bluetooth.BLE()
p = ble_simple_peripheral.BLESimplePeripheral(ble, name=NAME)

def on_rx(read):
    print("RX", read)

p.on_write(on_rx)
