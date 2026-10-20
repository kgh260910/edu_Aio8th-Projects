from machine import Pin, PWM, Timer

flash = PWM(Pin(4), freq=1000, duty=0)

duty = 0
step = 5  # 한 번에 바뀌는 크기
time_cnt = 0
ms_flag = False

def timer_callback(t):
    global ms_flag
    ms_flag = True

def timer_10ms():
    global duty, step
    duty += step
    if duty >= 300:  # 위 끝에 닿으면
        duty = 300
        step = -step  # 방향을 뒤집는다
    if duty <= 0:  # 아래 끝에 닿으면
        duty = 0
        step = -step
    flash.duty(duty)

tmr = Timer(0)
tmr.init(period=1, mode=Timer.PERIODIC, callback=timer_callback)

try:
    while True:
        if ms_flag:
            ms_flag = False
            time_cnt += 1

            if time_cnt % 10 == 0:
                timer_10ms()
except KeyboardInterrupt:
    tmr.deinit()
    flash.duty(0)
    flash.deinit()
    print("정지")
