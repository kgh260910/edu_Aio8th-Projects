import network
import time
import urequests
import json

ssid = "daduino"
password = "daduino12345"
stock_number = "005930"  # 삼성전자 종목 코드
url = f"https://m.stock.naver.com/api/stock/{stock_number}/integration"

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
    if wifi_connect():
        try:
            response = urequests.get(url)
            if response.status_code == 200:
                print("HTTP GET 요청 성공!")
                data = json.loads(response.text)

                # 주요 주식 데이터 추출
                stock_name = data["stockName"]
                last_close_price = next(item["value"] for item in data["totalInfos"] if item["code"] == "lastClosePrice")
                open_price = next(item["value"] for item in data["totalInfos"] if item["code"] == "openPrice")
                high_price = next(item["value"] for item in data["totalInfos"] if item["code"] == "highPrice")
                low_price = next(item["value"] for item in data["totalInfos"] if item["code"] == "lowPrice")
                market_value = next(item["value"] for item in data["totalInfos"] if item["code"] == "marketValue")
                per = next(item["value"] for item in data["totalInfos"] if item["code"] == "per")

                print("주식 이름:", stock_name)
                print("전일 종가:", last_close_price)
                print("시가:", open_price)
                print("고가:", high_price)
                print("저가:", low_price)
                print("시가총액:", market_value)
                print("PER:", per)
                
            else:
                print("HTTP GET 요청 실패. 상태 코드:", response.status_code)
        except Exception as e:
            print("HTTP GET 요청 중 오류 발생:", e)

if __name__ == "__main__":
    main()
