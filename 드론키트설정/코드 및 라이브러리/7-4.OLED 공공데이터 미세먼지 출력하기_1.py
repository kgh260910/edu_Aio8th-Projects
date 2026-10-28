import network
import time
import urequests

ssid = "daduino"
password = "daduino12345"
url = "https://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getCtprvnRltmMesureDnsty?serviceKey=fFWLxGIoKo8cQCIuS5Is1fVoiKXkdls%2FU5DSGRwzmbiwIBI0nlz5V6jllexlrGLKR9y8wV3E3i0SMPTLtAhyvw%3D%3D&returnType=json&numOfRows=100&pageNo=1&sidoName=%EC%84%9C%EC%9A%B8&ver=1.0" 
if url.startswith("https"):
    url = url.replace("https", "http", 1)


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
                print("Response:")
                print(response.text)
            else:
                print("HTTP GET 요청 실패. 상태 코드:", response.status_code)
        except Exception as e:
            print("HTTP GET 요청 중 오류 발생:", e)

if __name__ == "__main__":
    main()

