import network
import time
import urequests
import json
from machine import Pin
from machine import SoftI2C
from ssd1306 import SSD1306_I2C

# Wi-Fi 및 주식 데이터 URL 설정
ssid = "daduino"
password = "123456789"
stock_number = "005930"  # 삼성전자 종목 코드
url = f"https://m.stock.naver.com/api/stock/{stock_number}/integration"

# I2C 및 OLED 초기화
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
    while True:
        if wifi_connect():
            try:
                # 주식 데이터 요청
                response = urequests.get(url)
                if response.status_code == 200:
                    print("HTTP GET 요청 성공!")
                    data = json.loads(response.text)

                    # 주식 이름을 하드코딩
                    stock_name = "SAMSUNG"
                    current_price = next(item["value"] for item in data["totalInfos"] if item["code"] == "lastClosePrice")

                    # OLED에 출력
                    oled.fill(0)
                    oled.text("Stock Name:", 0, 10)
                    oled.text(stock_name, 0, 20)
                    oled.text("Price:", 0, 40)
                    oled.text(current_price, 0, 50)
                    oled.show()

                else:
                    print("HTTP GET 요청 실패. 상태 코드:", response.status_code)
            except Exception as e:
                print("HTTP GET 요청 중 오류 발생:", e)

        time.sleep(10.0)  # 1초마다 업데이트

if __name__ == "__main__":
    main()
