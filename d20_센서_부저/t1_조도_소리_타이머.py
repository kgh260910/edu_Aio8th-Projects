from machine import Pin, PWM, ADC, Timer

buzzer = PWM(Pin(6), freq=880, duty=0)
cds_sensor = ADC(Pin(8))
cds_sensor.atten(ADC.ATTN_11DB)

# ---- 내가 바꾸는 값 (s1_조도_소리.py 와 같다) ----
LIGHT_MIN = 340
LIGHT_MAX = 865
LEVELS = 20
DUTY_TABLE = [10, 12, 15, 19, 23, 28, 35, 43, 52, 65, 79, 98, 120, 148, 182, 224, 275, 338, 416, 512]

# ---- 인터럽트 깃발 : 알람 ----
ms = 0                           # 켠 뒤 지난 ms (인터럽트만 올린다)
flag_10 = False
flag_100 = False
flag_500 = False

def tick(t):                     # 1 ms 마다 저절로 불린다
    global ms, flag_10, flag_100, flag_500
    ms += 1
    if ms % 10 == 0:
        flag_10 = True
    if ms % 100 == 0:
        flag_100 = True
    if ms % 500 == 0:
        flag_500 = True

def light_level(value):          # s1 과 같은 함수
    level = (value - LIGHT_MIN) * LEVELS // (LIGHT_MAX - LIGHT_MIN) + 1
    return max(1, min(LEVELS, level))

beep_on = False                  # 지금 삑 울리는 중인가
value = 0
level = 1
duty = DUTY_TABLE[0]
last_look = 0                    # 밝기를 마지막으로 본 ms
look_gap = 0                     # 밝기를 다시 보기까지 걸린 ms

tmr = Timer(0)
tmr.init(period=1, mode=Timer.PERIODIC, callback=tick)

try:
    while True:
        if flag_10:                              # 10 ms : 소리 크기를 부저에 반영한다
            flag_10 = False
            if beep_on:
                buzzer.duty(duty)
            else:
                buzzer.duty(0)
        if flag_100:                             # 100 ms : 밝기를 읽는다
            flag_100 = False
            value = cds_sensor.read()
            level = light_level(value)
            duty = DUTY_TABLE[level - 1]
            look_gap = ms - last_look
            last_look = ms
        if flag_500:                             # 500 ms : 삑을 켜고 끄고, 쉘에 찍는다
            flag_500 = False
            beep_on = not beep_on
            print("조도", value, "-> 단계", level, "-> duty", duty, "| 센서를 다시 보기까지", look_gap, "ms")
except KeyboardInterrupt:
    pass
finally:
    tmr.deinit()
    buzzer.duty(0)
    buzzer.deinit()
