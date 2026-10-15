import network, time
from machine import Pin

SSID = "DW502iptime2G"                   # ★ 화면에 안내된 와이파이 이름으로 바꾼다
PASSWORD = "dw502502"                    # ★ 화면에 안내된 비밀번호로 바꾼다

red = Pin(33, Pin.OUT, value=1)                 # 빨간 LED: 0 이 켜짐

wlan = network.WLAN(network.STA_IF)
wlan.active(False)                              # 앞 실행에서 남은 접속 시도를 지우려고
time.sleep_ms(1000)                             # 껐다가 1초 쉬고
wlan.active(True)                               # 다시 켠다
wlan.connect(SSID, PASSWORD)                    # 공유기에 접속을 요청한다

print("연결 중", end="")
start = time.ticks_ms()
while not wlan.isconnected():  # wlan이 연결이 안되어있으면
    if time.ticks_diff(time.ticks_ms(), start) > 15000:     # 15초를 기다린다
        break
    print(".", end="")
    time.sleep_ms(500)

if wlan.isconnected():
    ip, mask, gateway, dns = wlan.ifconfig()    # 공유기가 나눠 준 네 가지 값
    red.value(0)                                # 연결되면 빨간 LED 를 켠다
    print("\n연결 성공!")     # \n : 줄바꿈
    print("보드 주소 (IP)     :", ip)
    print("같은 동네 범위     :", mask)
    print("나가는 문 (게이트웨이):", gateway)
    print("주소록 (DNS)       :", dns)
    print("신호 세기          :", wlan.status("rssi"), "dBm")
else:
    print("\n연결 실패 → 이름·비밀번호를 다시 확인하세요")

# ⭐ 도전: 연결에 성공하면 플래시 대신 빨간 LED 가 3번 깜빡이게 바꿔 보자.
