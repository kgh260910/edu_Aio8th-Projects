from machine import Pin, PWM , Timer
import time

M1_motor = PWM(Pin(4), freq = 10000 ,duty=0)
M2_motor = PWM(Pin(5), freq = 10000 ,duty=0)
M3_motor = PWM(Pin(40), freq = 10000 ,duty=0)
M4_motor = PWM(Pin(41), freq = 10000 ,duty=0)

time_cnt = 0
dutyy = 100
step = 20
ms_flag = False

def timer_callback(t):
    global ms_flag
    ms_flag = True
    
def timer_1000ms():
    global dutyy, step
    dutyy += step
    if dutyy >= 100:
        dutyy = 100
        step = -step
    if dutyy <= 0:
        dutyy = 0
        step = -step
        
    M1_motor.duty(dutyy)
    M2_motor.duty(dutyy)
    M3_motor.duty(dutyy)
    M4_motor.duty(dutyy)
        
tmr = Timer(0)
tmr.init(period=1, mode=Timer.PERIODIC, callback=timer_callback)

try:
    while True:
        if ms_flag:
            ms_flag = False
            time_cnt += 1
            
            if time_cnt % 1000 == 0:
                timer_1000ms()
        
        

except KeyboardInterrupt:
    M1_motor.deinit()
    M2_motor.deinit()
    M3_motor.deinit()
    M4_motor.deinit()
    print("코드를 종료합니다.")

