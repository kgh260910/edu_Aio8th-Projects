import bluetooth,ble_simple_peripheral
import time

ble = bluetooth.BLE()
p = ble_simple_peripheral.BLESimplePeripheral(ble,name='pyD_1234')

def on_rx(read):
    print("RX:", read)

p.on_write(on_rx)

cnt = 0
try:
    while True:
        if p.is_connected():
            p.send(str(cnt)+"\r\n")
            cnt += 1
        time.sleep(1.0)
except :
    pass