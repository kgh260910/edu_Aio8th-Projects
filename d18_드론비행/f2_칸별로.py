# f2_칸별로.py — 받은 값을 칸(인덱스)마다 나눠서 찍는다 (교재 3-1_2)
import bluetooth, ble_simple_peripheral, time

NAME = 'pyD_01'   # ← 내 번호로 바꾼다. 8글자 이하

ble = bluetooth.BLE()
p = ble_simple_peripheral.BLESimplePeripheral(ble, name=NAME)

def on_rx(read):
    print("=" * 50)
    for i in range(len(read)):
        print(i, read[i])
    print("=" * 50)

p.on_write(on_rx)
