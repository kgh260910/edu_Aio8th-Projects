import bluetooth, time
from machine import Pin, Timer

NAME = "CAM-DW502-김건희"                         # ★ 내 이름으로 바꾼다 (예: CAM-DW502-홍길동, 한글 5글자까지)
btn = Pin(0, Pin.IN, Pin.PULL_UP)               # 누르면 0
red = Pin(33, Pin.OUT, value=1)                 # 빨간 LED: 0 이 켜짐

# ── 블루투스: 글자를 주고받는 통로(UART 서비스) 하나를 만든다 ──
UART = bluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
TX = (bluetooth.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E"), bluetooth.FLAG_NOTIFY)   # 보드 → 폰
SERVICE = (UART, (TX,))

ble = bluetooth.BLE()
ble.active(True)
((tx_handle,),) = ble.gatts_register_services((SERVICE,))

conn = None                                     # 지금 연결된 폰 (없으면 None)
count = 0                                       # 버튼을 누른 횟수
btn_last = 1
flag_10ms = False
isr_cnt = 0

def make_payload(name):
    n = name.encode()
    return bytes([2, 0x01, 0x06]) + bytes([len(n) + 1, 0x09]) + n

def advertise():
    ble.gap_advertise(100_000, adv_data=make_payload(NAME))

def ble_irq(event, data):                       # 폰이 연결되거나 끊길 때 불리는 함수
    global conn
    if event == 1:                              # 1 = 폰이 연결됨
        conn = data[0]
        red.value(0)
        print("연결됨")
    elif event == 2:                            # 2 = 연결이 끊김
        conn = None
        red.value(1)
        print("끊김 → 다시 이름 알리기")
        advertise()

ble.irq(ble_irq)

def timer_isr(t):                               # 인터럽트는 깃발만 세운다
    global isr_cnt, flag_10ms
    isr_cnt += 1
    if isr_cnt % 10 == 0:
        flag_10ms = True
    if isr_cnt >= 1000:
        isr_cnt = 0

def task_10ms():
    global btn_last, count
    now = btn.value()
    if btn_last == 1 and now == 0:              # 눌린 순간만 잡는다
        count += 1
        msg = "누름 %d 김건희" % count
        print(msg)
        if conn is not None:
            ble.gatts_notify(conn, tx_handle, msg.encode())   # 폰으로 글자를 보낸다
    btn_last = now

tmr = Timer(0)
tmr.init(period=1, mode=Timer.PERIODIC, callback=timer_isr)
advertise()
print("이름 알리는 중:", NAME)

try:
    while True:
        if flag_10ms:
            flag_10ms = False
            task_10ms()
except KeyboardInterrupt:
    tmr.deinit()
    ble.gap_advertise(None)
    ble.active(False)
    red.value(1)
    print("정지")

# ⭐ 도전: 누를 때마다 "누름 3" 대신 내 이름을 보내 보자.
