import network
import time
import urequests

ssid = "daduino"
password = "daduino12345"
polling_interval = 10
url = "http://www.kma.go.kr/wid/queryDFSRSS.jsp?zone=4139054000" 

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

def extract_temp_and_reh(xml_text):
    try:
        temp_start = xml_text.find("<temp>") + len("<temp>")
        temp_end = xml_text.find("</temp>", temp_start)
        temp = xml_text[temp_start:temp_end]

        reh_start = xml_text.find("<reh>") + len("<reh>")
        reh_end = xml_text.find("</reh>", reh_start)
        reh = xml_text[reh_start:reh_end]

        return temp, reh
    except Exception as e:
        print("Error extracting data from XML:", e)
        return None, None

def main():
    while True:
        if wifi_connect():
            try:
                response = urequests.get(url)
                if response.status_code == 200:
                    print("HTTP GET 요청 성공!")

                    temp, reh = extract_temp_and_reh(response.text)
                    if temp is not None and reh is not None:
                        print("온도:", temp)
                        print("습도:", reh)
                else:
                    print("HTTP GET 요청 실패. 상태 코드:", response.status_code)
            except Exception as e:
                print("HTTP GET 요청 중 오류 발생:", e)

        time.sleep(polling_interval)

if __name__ == "__main__":
    main()
