import bluetooth, ble_simple_peripheral

# ───── ★ 고쳐 쓰는 값 ─────
NAME = "pyD_1234"        # 내 번호로 (영문·숫자 11글자까지)
MAX_DUTY = 200           # 앱에서 보내는 숫자의 위쪽 끝 (0 ~ 200)
INPUT_MODE = "text"      # "text": 글자 숫자 "150" 을 보낸다 · "byte": 숫자 1바이트를 보낸다
# ───── 여기까지 ─────

ble = bluetooth.BLE()
p = ble_simple_peripheral.BLESimplePeripheral(ble, name=NAME)

rx_data = None           # 폰이 보낸 것을 적어 두는 포스트잇
target = 0               # 폰이 정해 준 목표 듀티

def on_rx(read):         # 폰이 값을 써 넣으면 불린다 — 적어 두기만 한다
    global rx_data
    rx_data = read

p.on_write(on_rx)

def to_number(read):     # 받은 bytes 를 숫자로 바꾼다
    if INPUT_MODE == "byte":
        return read[0]
    return int(read.decode().strip())       # "150" → 150

def limit(n, lo, hi):    # 범위 밖이면 끝으로 붙인다
    if n < lo:
        return lo
    if n > hi:
        return hi
    return n

print("광고 중:", NAME)

try:
    while True:
        if rx_data is not None:
            data = rx_data
            rx_data = None
            try:
                target = limit(to_number(data), 0, MAX_DUTY)
                print("목표 듀티 =", target)
            except ValueError:
                print("숫자를 보내 주세요:", data)
except KeyboardInterrupt:
    print("정지")
