import network
import time
import urequests
import json
from machine import Pin
from machine import SoftI2C
from ssd1306 import SSD1306_I2C

ssid = "daduino"
password = "123456789"
url = "https://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getCtprvnRltmMesureDnsty?serviceKey=fFWLxGIoKo8cQCIuS5Is1fVoiKXkdls%2FU5DSGRwzmbiwIBI0nlz5V6jllexlrGLKR9y8wV3E3i0SMPTLtAhyvw%3D%3D&returnType=json&numOfRows=100&pageNo=1&sidoName=%EC%84%9C%EC%9A%B8&ver=1.0" 
if url.startswith("https"):
    url = url.replace("https", "http", 1)

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

def main():
    while True :
        if wifi_connect():
            try:
                response = urequests.get(url)
                if response.status_code == 200:
                    print("HTTP GET 요청 성공!")
                    data = json.loads(response.text)

                    items = data["response"]["body"]["items"]

                     # 각 항목을 출력
                    for item in items:
                        if item["stationName"] == "강남대로":  # 측정소명이 "강남대로"인 경우에만 출력
                            print("시도명:", item["sidoName"])
                            print("측정소명:", item["stationName"])
                            print("측정일시:", item["dataTime"])
                            print("미세먼지(PM10) 농도:", item["pm10Value"])
                            print("초미세먼지(PM2.5) 농도:", item["pm25Value"])
                            print("\n")
                            
                            time_str = str(item["dataTime"])
                            pm10Value_str = "pm10: " + str(item["pm10Value"])
                            pm25Value = "pm25: " + str(item["pm25Value"])
                            
                            oled.fill(0)
                            oled.text(time_str, 0, 10)
                            oled.text(pm10Value_str, 20, 20)
                            oled.text(pm25Value, 20, 30)
                            oled.show()
                    
                else:
                    print("HTTP GET 요청 실패. 상태 코드:", response.status_code)
            except Exception as e:
                print("HTTP GET 요청 중 오류 발생:", e)
        
        time.sleep(10.0)

if __name__ == "__main__":
    main()

