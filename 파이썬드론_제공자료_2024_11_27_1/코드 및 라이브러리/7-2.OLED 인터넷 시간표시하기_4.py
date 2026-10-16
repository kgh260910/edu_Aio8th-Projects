import network
import time
import ntptime
from machine import Pin
from machine import SoftI2C
from ssd1306 import SSD1306_I2C

ssid = "daduino"
password = "daduino12345"

i2c = SoftI2C(sda=Pin(43), scl=Pin(44))
oled = SSD1306_I2C(128, 64, i2c)

def wifi_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if not wlan.isconnected():
        print("Connecting to network...")
        wlan.connect(ssid, password)

        while not wlan.isconnected():
            time.sleep_ms(300)

        print("Connected to network:", wlan.ifconfig())
        return True
    else:
        print("Already connected to network:", wlan.ifconfig())
        return True

def set_time_from_ntp():
    try:
        ntptime.settime() 
        print("Time synchronized with NTP")
    except Exception as e:
        print("Failed to synchronize time with NTP:", str(e))

def get_kst_time():
    utc_time = time.time()
    kst_time = time.localtime(utc_time + 9 * 3600)  # 9시간 추가
    return kst_time

if wifi_connect():
    set_time_from_ntp() 

while True:
    rtc_time = get_kst_time()
    formatted_time = "{}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(
        rtc_time[0], rtc_time[1], rtc_time[2], rtc_time[3], rtc_time[4], rtc_time[5]
    )
    print("Current Time (KST):", formatted_time)
    
    yyyy_mm_dd = "{}-{:02d}-{:02d}".format(rtc_time[0], rtc_time[1], rtc_time[2])
    hh_mm_ss = "{:02d}:{:02d}:{:02d}".format(rtc_time[3], rtc_time[4], rtc_time[5])

    oled.fill(0)
    oled.text(yyyy_mm_dd, 20, 20)
    oled.text(hh_mm_ss, 20, 30)
    oled.show()
    
    time.sleep(1)

