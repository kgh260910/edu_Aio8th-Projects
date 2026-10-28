import bluetooth, ble_simple_peripheral
import time
from machine import Pin
import dht

ble = bluetooth.BLE()
p = ble_simple_peripheral.BLESimplePeripheral(ble, name='pyD_1234')

dht11 = dht.DHT11(Pin(18))

def on_rx(read):
    print("RX:", read)

p.on_write(on_rx)

previous_time = time.time()
send_interval = 2.0

try:
    while True:
        current_time = time.time() 
        if current_time - previous_time >= send_interval:
            previous_time = current_time
            if p.is_connected():
                dht11.measure()
                temp = dht11.temperature()
                humi = dht11.humidity()
                if (temp is None) or (humi is None):
                    print("센서 에러")
                else:
                    send_str = str(temp) + "," + str(humi) + "\r\n"
                    p.send(send_str)
except :
    pass
