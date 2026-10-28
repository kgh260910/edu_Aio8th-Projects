import bluetooth,ble_simple_peripheral
import time
from machine import Pin, PWM

ble = bluetooth.BLE()
p = ble_simple_peripheral.BLESimplePeripheral(ble,name='pyD_1234')

LED_RED = PWM(Pin(21), freq=1000, duty=0)
LED_GREEN = PWM(Pin(47), freq=1000, duty=0)
LED_BLUE = PWM(Pin(48), freq=1000, duty=0)

def on_rx(read):
    print("RX:", read)
    
    decoded_data = read.decode('utf-8').strip()
    print("Decoded:", decoded_data)
    
    split_data = decoded_data.split(",")
    
    if len(split_data) == 4 and split_data[0] == "RGB":
        r = int(split_data[1])
        g = int(split_data[2])
        b = int(split_data[3])
        LED_RED.duty(r)
        LED_GREEN.duty(g)
        LED_BLUE.duty(b)
        print(f"Setting RGB LED to Red: {r}, Green: {g}, Blue: {b}")
        
    else:
        print("Error: Invalid command. Expected 'RGB,R,G,B'")
    
p.on_write(on_rx)

try:
    while True:
        time.sleep(1.0)
except :
    pass
