from machine import Pin
import time
import dht

dht11=dht.DHT11(Pin(18))

try :
    while True:
        dht11.measure()  
        temp = dht11.temperature()
        humi = dht11.humidity()
        print(f"온도:{temp}°C  습도:{humi}RH")
        time.sleep(1.0)

except :
    pass