import bluetooth, time
from machine import Pin, PWM, Timer

NAME = "CAM-DW502-이름"                         # ★ 내 이름으로 바꾼다 (예: CAM-DW502-홍길동, 한글 5글자까지)
btn = Pin(0, Pin.IN, Pin.PULL_UP)               # 누르면 0
flash = PWM(Pin(4), freq=1000, duty=0)          # 플래시 밝기 0~1023 (직시 금지)
red = Pin(33, Pin.OUT, value=1)                 # 빨간 LED: 0 이 켜짐
BRIGHT = 60                                     # 약한 밝기

# ── 블루투스: 보드→폰(TX) 통로와 폰→보드(RX) 통로를 둘 다 만든다 ──
UART = bluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
TX = (bluetooth.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E"), bluetooth.FLAG_NOTIFY)
RX = (bluetooth.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E"),
      bluetooth.FLAG_WRITE | bluetooth.FLAG_WRITE_NO_RESPONSE)
SERVICE = (UART, (TX, RX))

ble = bluetooth.BLE()
ble.active(True)
((tx_handle, rx_handle),) = ble.gatts_register_services((SERVICE,))

conn = None
command = ""                                    # 폰이 보낸 글자를 적어 두는 포스트잇
btn_last = 1
flag_10ms = False
isr_cnt = 0

def make_payload(name):
    n = name.encode()
    return bytes([2, 0x01, 0x06]) + bytes([len(n) + 1, 0x09]) + n

def advertise():
    ble.gap_advertise(100_000, adv_data=make_payload(NAME))

def ble_irq(event, data):
    global conn, command
    if event == 1:                              # 폰이 연결됨
        conn = data[0]
        print("연결됨")
    elif event == 2:                            # 연결이 끊김
        conn = None
        print("끊김 → 다시 이름 알리기")
        advertise()
    elif event == 3:                            # 3 = 폰이 RX 에 글자를 써 넣음
        command = ble.gatts_read(rx_handle).decode().strip()   # 읽어서 포스트잇에 적어 둔다

ble.irq(ble_irq)

def send(msg):
    print(msg)
    if conn is not None:
        ble.gatts_notify(conn, tx_handle, msg.encode())

def timer_isr(t):
    global isr_cnt, flag_10ms
    isr_cnt += 1
    if isr_cnt % 10 == 0:
        flag_10ms = True
    if isr_cnt >= 1000:
        isr_cnt = 0

def task_10ms():
    global btn_last, command
    if command:                                 # 폰에서 온 명령이 있으면 처리한다
        if command == "1":
            flash.duty(BRIGHT)
            red.value(0)
            send("플래시 켜짐")
        elif command == "0":
            flash.duty(0)
            red.value(1)
            send("플래시 꺼짐")
        else:
            send("모르는 명령: " + command)
        command = ""                            # 처리했으니 포스트잇을 뗀다
    now = btn.value()
    if btn_last == 1 and now == 0:              # 보드 버튼 → 폰으로 알림
        send("보드 버튼 눌림")
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
    flash.duty(0)
    flash.deinit()
    ble.gap_advertise(None)
    ble.active(False)
    red.value(1)
    print("정지")

# ⭐ 도전: 폰에서 "2" 를 보내면 플래시가 더 밝아지게 command 처리를 한 칸 더 늘려 보자.
