import bluetooth,ble_simple_peripheral
import time

ble = bluetooth.BLE()
p = ble_simple_peripheral.BLESimplePeripheral(ble,name='pyD_1234')

def on_rx(read):
    print("RX:", read)
    
    decoded_data = read.decode('utf-8').strip()
    print("Decoded:", decoded_data)
    
    split_data = decoded_data.split(",")
    
    if len(split_data) == 4 and split_data[0] == "RGB":
        r = int(split_data[1])
        g = int(split_data[2])
        b = int(split_data[3])
        print(f"Setting RGB LED to Red: {r}, Green: {g}, Blue: {b}")
        
    else:
        print("Error: Invalid command. Expected 'RGB,R,G,B'")
    
p.on_write(on_rx)

try:
    while True:
        time.sleep(1.0)
except :
    pass