import network, socket, time
from machine import Pin, PWM

SSID = "여기에_와이파이_이름"                   # ★ 화면에 안내된 와이파이 이름으로 바꾼다
PASSWORD = "여기에_비밀번호"                    # ★ 화면에 안내된 비밀번호로 바꾼다
BRIGHT = 60                                     # 약한 밝기 (직시 금지)

flash = PWM(Pin(4), freq=1000, duty=0)
red = Pin(33, Pin.OUT, value=1)

wlan = network.WLAN(network.STA_IF)
wlan.active(False)                              # 앞 실행에서 남은 접속 시도를 지우려고
time.sleep_ms(1000)                             # 껐다가 1초 쉬고
wlan.active(True)                               # 다시 켠다
wlan.connect(SSID, PASSWORD)
while not wlan.isconnected():
    time.sleep_ms(300)
ip = wlan.ifconfig()[0]
red.value(0)
print("브라우저에 이 주소를 입력하세요 → http://" + ip)

def page(state):
    return ("HTTP/1.0 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n"
            "<html><body style='font-size:40px;text-align:center'>"
            "<h1>ESP32-CAM 플래시</h1><p>지금: <b>" + state + "</b></p>"
            "<p><a href='/on'>켜기</a> &nbsp; <a href='/off'>끄기</a></p>"
            "</body></html>")

server = socket.socket()
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(("0.0.0.0", 80))                    # 80번 문: 웹 주소의 기본 문
server.listen(2)

state = "꺼짐"
try:
    while True:
        client, addr = server.accept()          # 브라우저가 문을 두드릴 때까지 기다린다
        request = client.recv(512).decode()
        path = request.split(" ")[1] if " " in request else "/"
        print("요청:", addr[0], path)
        if path == "/on":
            flash.duty(BRIGHT)
            state = "켜짐"
        elif path == "/off":
            flash.duty(0)
            state = "꺼짐"
        client.send(page(state))
        client.close()
except KeyboardInterrupt:
    pass
finally:
    server.close()
    flash.duty(0)
    flash.deinit()
    red.value(1)
    print("정지")

# ⭐ 도전: 주소 끝에 /blink 를 붙이면 플래시가 3번 깜빡이게 만들어 보자.
