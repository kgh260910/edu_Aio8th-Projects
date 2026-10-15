import bluetooth, time
from machine import Pin

NAME = "CAM-DW502-김건희"                         # ★ 내 이름으로 바꾼다 (예: CAM-DW502-홍길동, 한글 5글자까지)
red = Pin(33, Pin.OUT, value=1)                 # 빨간 LED: 0 이 켜짐

def make_payload(name):
    flags = bytes([2, 0x01, 0x06])              # [길이, 종류 0x01=플래그, 내용] 폰이 찾을 수 있게 한다
    n = name.encode()
    full = bytes([len(n) + 1, 0x09]) + n        # [길이, 종류 0x09=전체 이름, 이름]
    return flags + full

ble = bluetooth.BLE()
ble.active(True)                                # 블루투스 안테나를 켠다 
ble.gap_advertise(100_000, adv_data=make_payload(NAME)) # 0.1초(100000us(마이크로세컨드))마다 "나 여기 있어요" 
red.value(0)                                    # 이름 알리는 중에는 빨간 LED 를 켜 둔다
print("이름 알리는 중:", NAME)

try:
    while True:
        time.sleep_ms(500)                      # 에너지를 아낄 수 있다.
except KeyboardInterrupt:
    ble.gap_advertise(None)                     # 이름 알리기를 멈춘다
    ble.active(False)
    red.value(1)
    print("정지")

# ⭐ 도전: NAME 을 내 이름 영문 이니셜로 바꿔서 폰 목록에서 내 보드만 찾아 보자.
