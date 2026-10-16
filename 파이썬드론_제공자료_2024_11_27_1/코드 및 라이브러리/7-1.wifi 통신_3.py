import network
import time

ssid = "daduino"
password = "daduino12345"
static_ip = "192.168.0.150"  # 원하는 고정 IP 주소 설정
subnet_mask = "255.255.255.0" 
gateway = "192.168.0.1" 
dns_server = "8.8.8.8" 

def wifi_connect():
    wlan = network.WLAN(network.STA_IF)  
    wlan.active(True) 

    if not wlan.isconnected():
        print("Connecting to network...")
        wlan.active(True) 
        wlan.config(dhcp_hostname="my-esp32") 
        wlan.ifconfig((static_ip, subnet_mask, gateway, dns_server)) 
        wlan.connect(ssid, password) 

        while not wlan.isconnected():
            time.sleep_ms(300)

        print("Connected to network:", wlan.ifconfig())
        return True
    else:
        print("Already connected to network:", wlan.ifconfig())
        return True

if wifi_connect():
    pass

