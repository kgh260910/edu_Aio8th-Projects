import network
import time

ap_ssid = "pyDrone1234"    

def wifi_ap_mode():
    ap = network.WLAN(network.AP_IF)  
    ap.config(essid=ap_ssid)
    ap.active(True) 

wifi_ap_mode()  
