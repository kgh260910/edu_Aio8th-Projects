import bluetooth,ble_simple_peripheral
import time

ble = bluetooth.BLE()
p = ble_simple_peripheral.BLESimplePeripheral(ble,name='pyD_1234')

def on_rx(read):
    print("RX:", read)
    
    decoded_data = read.decode('utf-8').strip()
    print("Decoded:", decoded_data)
    
    split_data = decoded_data.split(",")
    print("Split Data:", split_data)

p.on_write(on_rx)

try:
    while True:
        time.sleep(1.0)
except :
    pass