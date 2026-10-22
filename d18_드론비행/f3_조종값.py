# f3_조종값.py — 칸을 조종 값(rol·pit·yaw·thr)과 명령으로 풀어 찍는다 (교재 3-2_1·3-2_2)
# 드론(drone 모듈)은 아직 부르지 않는다 — 모터는 돌지 않는다.
import bluetooth, ble_simple_peripheral, time

NAME = 'pyD_01'   # ← 내 번호로 바꾼다. 영문·숫자 8글자 이하

ble = bluetooth.BLE()
p = ble_simple_peripheral.BLESimplePeripheral(ble, name=NAME)

def on_rx(read):
    control_data = [None] * 4
    for i in range(4):
        control_data[i] = read[i + 1] - 100      # 0~200 으로 온 값을 -100~100 으로

    print("=" * 50)
    print("rol:", control_data[0])
    print("pit:", control_data[1])
    print("yaw:", control_data[2])
    print("thr:", control_data[3])

    if read[5] == 136:
        print('stop')
    elif read[5] == 24:
        print('take_off')
    elif read[5] == 72:
        print('landing')
    elif read[5] == 40:
        print('calibration')
    elif read[5] == 1:
        print('button1')
    elif read[5] == 2:
        print('button2')
    elif read[5] == 3:
        print('button3')
    elif read[5] == 4:
        print('button4')
    print("=" * 50)

p.on_write(on_rx)
