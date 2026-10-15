import network, socket, time, jpeg, machine
from camera import Camera, FrameSize, PixelFormat

machine.freq(240000000)                         # 보드 두뇌(CPU) 속도를 가장 빠른 240MHz 로 맞춘다

SSID = "여기에_와이파이_이름"                   # ★ 화면에 안내된 와이파이 이름으로 바꾼다
PASSWORD = "여기에_비밀번호"                    # ★ 화면에 안내된 비밀번호로 바꾼다

SIZE = FrameSize.QVGA                           # 크기: QQVGA < QVGA < VGA < XGA (XGA 는 OV2640 만, 느림)
QUALITY = 60                                    # 화질 0~100 (높을수록 선명하고 느림, 95 까지)

wlan = network.WLAN(network.STA_IF)
wlan.active(False)                              # 앞 실행에서 남은 접속 시도를 지우려고
time.sleep_ms(1000)                             # 껐다가 1초 쉬고
wlan.active(True)                               # 다시 켠다
wlan.connect(SSID, PASSWORD)
while not wlan.isconnected():
    time.sleep_ms(300)
ip = wlan.ifconfig()[0]


def open_camera(pixel_format, frame_size, xclk_mhz):
    # xclk_freq : 카메라 박자(MHz). 색 데이터는 10 으로 느리게
    for _ in range(3):                          # 카메라가 가끔 한 번에 안 켜져서 3번까지 다시 해 본다
        try:
            return Camera(pixel_format=pixel_format, frame_size=frame_size,
                          jpeg_quality=QUALITY, xclk_freq=xclk_mhz * 1000000)
        except OSError:
            time.sleep_ms(500)
    raise SystemExit("카메라가 안 켜졌습니다. 보드의 RST 버튼을 누르고 다시 실행하세요")


# 1) 일단 작게 켜서 카메라 센서 이름을 알아낸다
cam = open_camera(PixelFormat.RGB565, FrameSize.QQVGA, 10)
SENSOR = cam.sensor_name
cam.deinit()
time.sleep_ms(300)

# 2) 센서에 맞는 방식으로 다시 켠다
if SENSOR == "OV2640":
    # OV2640 은 센서가 JPEG 를 직접 만든다 (빠르다)
    cam = open_camera(PixelFormat.JPEG, SIZE, 24)       # 24MHz (20 은 와이파이가 느려졌다)
    encoder = None
else:
    # OV3660 등은 색 데이터(RGB565)로 찍고 보드가 JPEG 로 줄인다
    cam = open_camera(PixelFormat.RGB565, SIZE, 10)
    encoder = jpeg.Encoder(width=cam.get_pixel_width(), height=cam.get_pixel_height(),
                           pixel_format="RGB565_BE", quality=QUALITY)
if SENSOR == "OV2640":
    cam.set_vflip(True)                         # 이 보드는 카메라가 거꾸로 달려 있어 뒤집는다
if SENSOR == "OV3660":
    cam.set_wb_mode(3)                          # 화이트밸런스 '사무실'(3): 흰색이 분홍으로 기우는 것을 줄임
    for _ in range(5):                          # 설정이 반영되도록 몇 장 버린다
        cam.capture()
cam.capture()                                   # 첫 장은 밝기가 덜 맞아서 버린다
print("센서:", SENSOR, "→", "센서 JPEG 직접" if encoder is None else "RGB565 + 보드에서 JPEG 압축",
      "/ 화면 크기:", cam.get_pixel_width(), "x", cam.get_pixel_height())
print("브라우저에 이 주소를 입력하세요 → http://" + ip)

PAGE = (b"HTTP/1.0 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n"
        b"<html><body style='font-size:32px;text-align:center'>"
        b"<h1>ESP32-CAM 실시간 영상</h1><img src='/stream' style='width:640px'>"
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
        if path == "/stream":
            client.send(b"HTTP/1.0 200 OK\r\n"
                        b"Content-Type: multipart/x-mixed-replace; boundary=frame\r\n\r\n")
            try:
                while True:                     # 사진을 쉬지 않고 이어서 보낸다 = 영상
                    photo = cam.capture()
                    if encoder:
                        photo = encoder.encode(photo)
                    client.send(b"--frame\r\nContent-Type: image/jpeg\r\n"
                                b"Content-Length: %d\r\n\r\n" % len(photo))
                    client.send(photo)
                    client.send(b"\r\n")
            except OSError:
                print("브라우저가 닫혔습니다")   # 탭을 닫으면 여기로 온다
        else:
            client.send(PAGE)
        client.close()
except KeyboardInterrupt:
    pass
finally:
    server.close()
    cam.deinit()
    print("정지")

# ⭐ 도전: SIZE 를 FrameSize.VGA 나 FrameSize.XGA 로 바꿔 보자. 센서에 따라 영상이 얼마나 느려지는지 비교해 보자.
