from machine import Timer                       # machine 에서 부품 도구(클래스)를 가져온다 : Timer(타이머)

# 인터럽트가 세우는 깃발 : 시간 단위마다 하나씩
ms = 0                           # 켠 뒤 지난 ms (인터럽트만 올린다)
flag_10 = False
flag_50 = False
flag_100 = False
flag_500 = False

def tick(t):                     # 1 ms 마다 저절로 불린다
    global ms, flag_10, flag_50, flag_100, flag_500  # global : 이 함수 안에서 바깥 변수의 값을 바꾼다고 알린다
    ms += 1
    if ms % 10 == 0:
        flag_10 = True
    if ms % 50 == 0:
        flag_50 = True
    if ms % 100 == 0:
        flag_100 = True
    if ms % 500 == 0:
        flag_500 = True          # 깃발만 세우고 바로 빠져나간다

count_10 = 0
count_50 = 0
count_100 = 0
count_500 = 0

# tmr 객체 만들기 : Timer 클래스로 0번 하드웨어 타이머를 쓴다
tmr = Timer(0)
# init() 메서드로 타이머를 켠다 : period=1 = 1 ms 마다, mode=Timer.PERIODIC = 계속 반복, callback=tick = 때마다 tick 함수를 부른다
tmr.init(period=1, mode=Timer.PERIODIC, callback=tick)

try:
    while ms < 5005:             # 5초 동안 깃발이 몇 번 서는지 센다 (5000 ms 에 서는 마지막 깃발까지 받도록 5 ms 더)
        # 메인은 깃발이 서 있는지만 본다. 내리고 나서 일을 한다
        if flag_10:
            flag_10 = False
            count_10 += 1
        if flag_50:
            flag_50 = False
            count_50 += 1
        if flag_100:
            flag_100 = False
            count_100 += 1
        if flag_500:
            flag_500 = False
            count_500 += 1
            print("0.5초 깃발", count_500, "번째")
finally:                                        # 끝날 때 꼭 실행된다 : 부저와 타이머를 정리한다
    tmr.deinit()                                # deinit() 메서드 : 타이머를 끈다

print("5초 동안 깃발 : 10ms", count_10, "번, 50ms", count_50, "번, 100ms", count_100, "번, 500ms", count_500, "번")
