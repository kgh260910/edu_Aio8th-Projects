from machine import Pin, PWM, ADC, Timer        # machine 에서 부품 도구(클래스)를 가져온다 : Pin(핀), PWM(부저), ADC(조도센서 읽기), Timer(타이머)

# 부저 객체 만들기 : PWM 클래스(설계도)로 buzzer 를 만든다
#   Pin(6) = 6번 핀에 달린 부저, freq=880 = 소리 높이 880 Hz, duty=0 = 처음에는 소리 끔 (0~1023)
buzzer = PWM(Pin(6), freq=880, duty=0)
# 조도센서 객체 만들기 : ADC 클래스(숫자로 읽는 설계도)로 cds_sensor 를 만든다. Pin(8) = 8번 핀(보드 표기 IO8)
cds_sensor = ADC(Pin(8))
cds_sensor.atten(ADC.ATTN_11DB)                 # atten() 메서드 : 읽는 전압 범위를 가장 넓게(11 dB) 맞춘다 -> 값이 0~4095

# ---- 내가 바꾸는 값 (s1_조도_소리.py 와 같다) ----
LIGHT_MIN = 340
LIGHT_MAX = 865
LEVELS = 20
DUTY_TABLE = [10, 12, 13, 15, 18, 20, 24, 27, 31, 36, 42, 48, 55, 64, 73, 85, 98, 113, 130, 150]

# ---- 인터럽트 깃발 : 알람 ----
ms = 0                           # 켠 뒤 지난 ms (인터럽트만 올린다)
flag_10 = False
flag_100 = False
flag_500 = False

def tick(t):                     # 1 ms 마다 저절로 불린다
    global ms, flag_10, flag_100, flag_500      # global : 이 함수 안에서 바깥 변수의 값을 바꾼다고 알린다
    ms += 1
    if ms % 10 == 0:
        flag_10 = True
    if ms % 100 == 0:
        flag_100 = True
    if ms % 500 == 0:
        flag_500 = True

def light_level(value):          # s1 과 같은 함수
    level = (value - LIGHT_MIN) * LEVELS // (LIGHT_MAX - LIGHT_MIN)
    if level < 0:
        level = 0
    if level > LEVELS - 1:
        level = LEVELS - 1
    return level

beep_on = False                  # 지금 삑 울리는 중인가
value = 0
level = 0
duty = DUTY_TABLE[0]

# tmr 객체 만들기 : Timer 클래스로 0번 하드웨어 타이머를 쓴다
tmr = Timer(0)
# init() 메서드로 타이머를 켠다 : period=1 = 1 ms 마다, mode=Timer.PERIODIC = 계속 반복, callback=tick = 때마다 tick 함수를 부른다
tmr.init(period=1, mode=Timer.PERIODIC, callback=tick)

try:
    while True:
        if flag_10:                              # 10 ms : 소리 크기를 부저에 반영한다
            flag_10 = False
            if beep_on:
                buzzer.duty(duty)               # duty() 메서드 : 소리 크기를 정한다 (켜짐)
            else:
                buzzer.duty(0)                  # duty(0) : 소리를 끈다
        if flag_100:                             # 100 ms : 밝기를 읽는다
            flag_100 = False
            value = cds_sensor.read()           # read() 메서드 : 밝기를 숫자(0~4095)로 읽는다
            level = light_level(value)
            duty = DUTY_TABLE[level]
        if flag_500:                             # 500 ms : 삑을 켜고 끄고, 쉘에 찍는다
            flag_500 = False
            beep_on = not beep_on
            print("조도", value, "-> 단계", level, "-> duty", duty)
except KeyboardInterrupt:                       # 정지 버튼(Ctrl + C)을 누르면 여기로 온다
    pass
finally:                                        # 끝날 때 꼭 실행된다 : 부저와 타이머를 정리한다
    tmr.deinit()                                # deinit() 메서드 : 타이머를 끈다
    buzzer.duty(0)                              # duty(0) : 소리를 끈다
    buzzer.deinit()                             # deinit() 메서드 : 부저를 놓아 준다 (끝낼 때)
