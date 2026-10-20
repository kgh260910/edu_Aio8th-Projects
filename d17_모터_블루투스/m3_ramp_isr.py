import bluetooth, ble_simple_peripheral
from machine import Pin, PWM, Timer

# ───── ★ 고쳐 쓰는 값: 이 칸의 숫자만 바꾸면 된다 ─────
NAME = "pyD_1234"        # 내 번호로 (영문·숫자 11글자까지)
MAX_DUTY = 200           # 앱에서 보내는 숫자의 위쪽 끝 (0 ~ 200)
STEP = 1                 # 100ms 마다 바뀌는 듀티 크기
PWM_FREQ = 10000         # PWM 주파수 (교재 2-4 와 같다)
INPUT_MODE = "text"      # "text": 글자 숫자 "150" 을 보낸다 · "byte": 숫자 1바이트를 보낸다
# ───── 여기까지 ─────

M1_motor = PWM(Pin(4), freq=PWM_FREQ, duty=0)    # 1번 모터
M2_motor = PWM(Pin(5), freq=PWM_FREQ, duty=0)    # 2번 모터
M3_motor = PWM(Pin(40), freq=PWM_FREQ, duty=0)   # 3번 모터
M4_motor = PWM(Pin(41), freq=PWM_FREQ, duty=0)   # 4번 모터

ble = bluetooth.BLE()
p = ble_simple_peripheral.BLESimplePeripheral(ble, name=NAME)

rx_data = None           # 폰이 보낸 것을 적어 두는 포스트잇
target = 0               # 폰이 정해 준 목표 듀티
duty = 0                 # 지금 듀티

# 인터럽트가 세우는 깃발: 시간 단위마다 하나씩
flag_10ms = False
flag_100ms = False
flag_500ms = False

isr_cnt = 0              # 인터럽트가 세는 ms (메인은 건드리지 않는다)

def timer_isr(t):
    global isr_cnt, flag_10ms, flag_100ms, flag_500ms
    isr_cnt += 1
    if isr_cnt % 10 == 0:
        flag_10ms = True
    if isr_cnt % 100 == 0:
        flag_100ms = True
    if isr_cnt >= 500:
        flag_500ms = True
        isr_cnt = 0
    # 깃발만 세우고 바로 빠져나간다

def on_rx(read):
    global rx_data
    rx_data = read

p.on_write(on_rx)

def to_number(read):
    if INPUT_MODE == "byte":
        return read[0]
    return int(read.decode().strip())

def limit(n, lo, hi):
    if n < lo:
        return lo
    if n > hi:
        return hi
    return n

def move_toward(now, goal, step):    # now 에서 goal 쪽으로 step 만큼만 한 걸음
    if now < goal:
        return min(now + step, goal)
    if now > goal:
        return max(now - step, goal)
    return now

def set_duty(d1, d2, d3, d4):        # 모터마다 듀티를 하나씩 직접 정해 준다
    M1_motor.duty(d1)
    M2_motor.duty(d2)
    M3_motor.duty(d3)
    M4_motor.duty(d4)

def task_10ms():                     # 10ms 마다 : 폰이 보낸 값을 확인한다
    global rx_data, target
    if rx_data is not None:
        data = rx_data
        rx_data = None
        try:
            target = limit(to_number(data), 0, MAX_DUTY)
            print("목표 듀티 =", target)
        except ValueError:
            print("숫자를 보내 주세요:", data)

def task_100ms():                    # 100ms 마다 : 목표 쪽으로 한 걸음
    global duty
    goal = target if p.is_connected() else 0      # 폰과 끊어지면 목표를 0 으로
    new = move_toward(duty, goal, STEP)
    if new != duty:
        duty = new
        set_duty(duty, duty, duty, duty)
        if duty == 0:
            print("모터 꺼짐")

def task_500ms():                    # 500ms 마다 : 지금 상태를 알려 준다
    if duty != target:
        print("목표", target, " 현재", duty)

tmr = Timer(0)
tmr.init(period=1, mode=Timer.PERIODIC, callback=timer_isr)
print("광고 중:", NAME)

try:
    while True:
        # 메인은 깃발이 서 있는지만 본다. 내리고 나서 일을 한다
        if flag_10ms:
            flag_10ms = False
            task_10ms()
        if flag_100ms:
            flag_100ms = False
            task_100ms()
        if flag_500ms:
            flag_500ms = False
            task_500ms()
except KeyboardInterrupt:
    tmr.deinit()
    set_duty(0, 0, 0, 0)
    M1_motor.deinit()
    M2_motor.deinit()
    M3_motor.deinit()
    M4_motor.deinit()
    print("정지 — 모터 꺼짐")
