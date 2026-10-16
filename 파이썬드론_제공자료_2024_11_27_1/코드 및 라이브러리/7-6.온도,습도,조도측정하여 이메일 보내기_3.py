import umail
import network
import time
from machine import Pin, ADC
import dht

# Wi-Fi 설정
ssid = 'daduino'
password = 'daduino12345'

# 이메일 설정
sender_email = 'munjjac@gmail.com'  # 보내는 사람 이메일
sender_name = 'prDrone'  # 보내는 사람 이름
sender_app_password = 'oxes wswv yuqv psxd'  # 구글 앱 비밀번호
recipient_email = 'munjjac@hanmail.net'  # 받는 사람 이메일
email_subject = 'Sensor Data Report'  # 이메일 제목

# 온습도 센서(DHT11) 설정
dht11 = dht.DHT11(Pin(18))

# 조도 센서 설정
cds_sensor = ADC(Pin(8))
cds_sensor.atten(ADC.ATTN_11DB)

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

def get_sensor_data():
    """온도, 습도, 조도 데이터를 측정합니다."""
    try:
        # 온도와 습도 측정
        dht11.measure()
        temp = dht11.temperature()
        humi = dht11.humidity()

        # 조도 측정
        cds_value = cds_sensor.read()

        return temp, humi, cds_value
    except Exception as e:
        print(f"센서 데이터를 가져오는 중 오류 발생: {e}")
        return None, None, None

def send_email(sender_email, sender_app_password, sender_name, recipient_email, email_subject, message):
    """이메일 전송"""
    smtp = umail.SMTP('smtp.gmail.com', 587, ssl=False)
    smtp.login(sender_email, sender_app_password)
    smtp.to(recipient_email)
    smtp.write(f"From:{sender_name} <{sender_email}>\n")
    smtp.write(f"Subject:{email_subject}\n")
    smtp.write(message)
    smtp.send()
    smtp.quit()
    print("메일을 성공적으로 보냈습니다.")

def main():
    if wifi_connect():
        # 센서 데이터 가져오기
        temp, humi, cds_value = get_sensor_data()

        if temp is not None and humi is not None and cds_value is not None:
            # 이메일에 포함할 메시지 작성
            message = f"Hello from ESP32\n\nTemperature: {temp}C\nHumidity: {humi}%\nLight Intensity: {cds_value}\n"

            print("보낼 이메일 내용:")
            print(message)

            # 이메일 전송
            send_email(sender_email, sender_app_password, sender_name, recipient_email, email_subject, message)
        else:
            print("센서 데이터를 가져올 수 없어 이메일을 보내지 못했습니다.")

if __name__ == "__main__":
    main()
