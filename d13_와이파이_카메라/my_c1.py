import network, socket, time
from camera import Camera, FrameSize, PixelFormat

SSID = "DW502iptime2G"                   # ★ 화면에 안내된 와이파이 이름으로 바꾼다
PASSWORD = "dw502502"                    # ★ 화면에 안내된 비밀번호로 바꾼다

wlan = network.WLAN(network.STA_IF)
wlan.active(False)                              # 앞 실행에서 남은 접속 시도를 지우려고
time.sleep_ms(1000)                             # 껐다가 1초 쉬고
wlan.active(True)                               # 다시 켠다
wlan.connect(SSID, PASSWORD)
while not wlan.isconnected():
    time.sleep_ms(300)
ip = wlan.ifconfig()[0]

# 카메라를 JPEG(사진 파일 형식)로 켠다. 처음부터 JPEG 로 켜야 브라우저가 읽는다.
cam = Camera(pixel_format=PixelFormat.JPEG, frame_size=FrameSize.QVGA)   # QVGA = 320x240
print("브라우저에 이 주소를 입력하세요 → http://" + ip)

PAGE = (b"HTTP/1.0 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n"
        b"<html><body style='font-size:32px;text-align:center'>"
        b"<h1>ESP32-CAM 사진</h1><img src='/capture'><p><a href='/'>새 사진 찍기</a></p>"
        b"</body></html>")

server = socket.socket()
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(("0.0.0.0", 80))
server.listen(2)

try:
    while True:
        client, addr = server.accept()
        request = client.recv(512).decode()
        path = request.split(" ")[1] if " " in request else "/"
        print("요청:", addr[0], path)
        if path == "/capture":
            photo = cam.capture()               # 사진 한 장 = JPEG 바이트 덩어리
            client.send(b"HTTP/1.0 200 OK\r\nContent-Type: image/jpeg\r\n"
                        b"Cache-Control: no-store\r\nContent-Length: %d\r\n\r\n" % len(photo))
            client.send(photo)
        else:
            client.send(PAGE)
        client.close()
except KeyboardInterrupt:
    pass
finally:
    server.close()
    cam.deinit()
    print("정지")

# ⭐ 도전: FrameSize.QVGA 를 FrameSize.VGA 로 바꿔 사진이 얼마나 커지는지 비교해 보자.
