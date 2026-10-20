from machine import Pin, PWM, Timer

flash = PWM(Pin(4), freq=1000, duty=0)

MIN_DUTY = 10  # 가장 어두운 밝기 (0 ~ 1023)
MAX_DUTY = 300  # 가장 밝은 밝기 (0 ~ 1023)
STEPS = 100  # 어두움 → 밝음을 100칸으로 나눈다
UPDATE_MS = 20  # 몇 ms 마다 한 칸 움직일지

level = 0  # 0 ~ STEPS 사이의 칸 번호
direction = 1  # 1 이면 밝아지고, -1 이면 어두워진다
time_cnt = 0
ms_flag = False

def timer_callback(t):
    global ms_flag
    ms_flag = True

def level_to_duty(lv):
    # 제곱 곡선: 어두운 쪽은 천천히, 밝은 쪽은 빠르게 올라간다
    return MIN_DUTY + (MAX_DUTY - MIN_DUTY) * lv * lv // (STEPS * STEPS)

def fade_step():
    global level, direction
    level += direction
    if level >= STEPS or level <= 0:
        direction = -direction
    flash.duty(level_to_duty(level))

tmr = Timer(0)
tmr.init(period=1, mode=Timer.PERIODIC, callback=timer_callback)

try:
    while True:
        if ms_flag:
            ms_flag = False
            time_cnt += 1

            if time_cnt % UPDATE_MS == 0:
                fade_step()
except KeyboardInterrupt:
    tmr.deinit()
    flash.duty(0)
    flash.deinit()
    print("정지")
