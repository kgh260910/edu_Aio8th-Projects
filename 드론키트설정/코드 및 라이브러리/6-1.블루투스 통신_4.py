import bluetooth, ble_simple_peripheral
import time
from machine import Pin
import dht

ble = bluetooth.BLE()
p = ble_simple_peripheral.BLESimplePeripheral(ble, name='pyD_1234')

dht11 = dht.DHT11(Pin(18))

key1 = Pin(38, Pin.IN, Pin.PULL_UP)
prev_state1 = key1.value()
key2 = Pin(39, Pin.IN, Pin.PULL_UP)
prev_state2 = key2.value()

def on_rx(read):
    print("RX:", read)

p.on_write(on_rx)

def get_key1():
    global prev_state1
    current_state = key1.value() 
    if current_state != prev_state1:
        prev_state1 = current_state
        if current_state == 0:
            return 1
    else:
        return 0

def get_key2():
    global prev_state2
    current_state = key2.value() 
    if current_state != prev_state2:
        prev_state2 = current_state
        if current_state == 0:
            return 1
    else:
        return 0

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
        
        if get_key1():
            p.send("key1 click\r\n")
            time.sleep(0.1)
    
        if get_key2():
            p.send("key2 click\r\n")
            time.sleep(0.1)
except :
    pass

