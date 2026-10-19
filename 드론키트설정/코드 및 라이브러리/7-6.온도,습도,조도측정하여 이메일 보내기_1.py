import umail
import network
import time

ssid = 'daduino'
password = 'daduino12345'

sender_email = 'munjjac@gmail.com' #구글 ID test@gmail.com 형식
sender_name = 'prDrone' #보내는 사람 이름
sender_app_password = 'oxes wswv yuqv psxd' #구글 앱 비밀번호
recipient_email ='munjjac@hanmail.net' #받는 사람 이메일주소
email_subject ='Test Email' #이메일 제목

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
        smtp = umail.SMTP('smtp.gmail.com', 587, ssl=False)
        smtp.login(sender_email, sender_app_password)
        smtp.to(recipient_email)
        smtp.write("From:" + sender_name + "<"+ sender_email+">\n")
        smtp.write("Subject:" + email_subject + "\n")
        smtp.write("Hello from ESP32")
        smtp.send()
        smtp.quit()
        print("메일을 성공적으로 보냈습니다.")

if __name__ == "__main__":
    main()