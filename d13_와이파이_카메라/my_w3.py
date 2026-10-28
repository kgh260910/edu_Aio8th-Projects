import network, socket, time
from machine import Pin, PWM

SSID = "DW502iptime2G"                   # ★ 화면에 안내된 와이파이 이름으로 바꾼다
PASSWORD = "dw502502"                    # ★ 화면에 안내된 비밀번호로 바꾼다
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
print("브라우저에 이 주소를 입력하세요 → http://" + ip + "/blink")

def blink():
    flash.duty(BRIGHT)
    time.sleep_ms(100)
    flash.duty(0)
    time.sleep_ms(100)
    flash.duty(BRIGHT)
    time.sleep_ms(100)
    flash.duty(0)
    time.sleep_ms(100)
    flash.duty(BRIGHT)
    time.sleep_ms(100)
    flash.duty(0)
    time.sleep_ms(100)
    state = "blink"

def page(state):
    return ("HTTP/1.0 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n"
            "<html><body style='font-size:40px;text-align:center'>"
            "<h1>ESP32-CAM 플래시</h1><p>지금: <b>" + state + "</b></p>"
            "<p><a href='/on'>켜기</a> &nbsp; <a href='/off'>끄기</a></p>"
            "<a href='/blink'>blink</a>"
            "</body></html>")
# charset=utf-8 안 넣으면 한글 등이 깨져 보일 수 있다.
#가독성 좋게 만들기 ?

server = socket.socket()
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(("0.0.0.0", 80))                    # 80번 문: 웹 주소의 기본 문
server.listen(2)                   # 2명만 받겠다

state = "꺼짐"
try:
    while True:
        client, addr = server.accept()          # 브라우저가 문을 두드릴 때까지 기다린다
        request = client.recv(512).decode() #클라이언트가 보낸 데이터를 최대512byte까지 읽어오겠다
        path = request.split(" ")[1] if " " in request else "/"
        # if " " in request:
            # path = request.split(" ")[1]
        # else:
            # path = "/"
        print("요청:", addr[0], path)
        if path == "/on":
            flash.duty(BRIGHT)
            state = "켜짐"
        elif path == "/off":
            flash.duty(0)
            state = "꺼짐"
        elif path == "/blink":
            blink()
    
            
        client.send(page(state))  # 클라이언트에게 page(state)를 보냅니다.
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

