from machine import Timer

# 인터럽트가 세우는 깃발 : 시간 단위마다 하나씩
ms = 0                           # 켠 뒤 지난 ms (인터럽트만 올린다)
flag_10 = False
flag_50 = False
flag_100 = False
flag_500 = False

def tick(t):                     # 1 ms 마다 저절로 불린다
    global ms, flag_10, flag_50, flag_100, flag_500
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

tmr = Timer(0)
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
finally:
    tmr.deinit()

print("5초 동안 깃발 : 10ms", count_10, "번, 50ms", count_50, "번, 100ms", count_100, "번, 500ms", count_500, "번")
