from machine import Pin, Timer
import time

flash = Pin(4, Pin.OUT, value=0)
red = Pin(33, Pin.OUT, value=1)

# 인터럽트가 세우는 깃발: 시간 단위마다 하나씩
flag_10ms = False
flag_100ms = False
flag_500ms = False
flag_1000ms = False

isr_cnt = 0  # 인터럽트가 세는 ms (메인은 건드리지 않는다)

def timer_isr(t):
    global isr_cnt, flag_10ms, flag_100ms, flag_500ms, flag_1000ms
    isr_cnt += 1
    if isr_cnt % 10 == 0:
        flag_10ms = True
    if isr_cnt % 100 == 0:
        flag_100ms = True
    if isr_cnt % 500 == 0:
        flag_500ms = True
    if isr_cnt >= 1000:
        flag_1000ms = True
        isr_cnt = 0
    # 깃발만 세우고 바로 빠져나간다

def task_10ms():
    pass

def task_100ms():
    flash.value(flash.value() ^ 1)

def task_500ms():
    red.value(red.value() ^ 1)

def task_1000ms():
    print("1초 경과")

tmr = Timer(0)
tmr.init(period=1, mode=Timer.PERIODIC, callback=timer_isr)

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
        if flag_1000ms:
            flag_1000ms = False
            task_1000ms()
except KeyboardInterrupt:
    tmr.deinit()
    flash.value(0)
    red.value(1)
    print("타이머 정지")
