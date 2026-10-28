from machine import Pin
import time

key = Pin(0, Pin.IN, Pin.PULL_UP)
prev_key = key.value()

def get_key():
    global  prev_key
    curr_key = key.value()
    if curr_key != prev_key:
        prev_key = curr_key
        if curr_key == 0:
            return True
        time.sleep(0.1)
        
    return False

try:
    while True:
        if get_key():
            print("버튼이 눌렸습니다")

except KeyboardInterrupt:
    print("코드를 종료합니다.")