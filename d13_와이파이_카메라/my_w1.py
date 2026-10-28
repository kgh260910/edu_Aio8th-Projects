import network

wlan = network.WLAN(network.STA_IF)             # 보드를 '손님(STA)' 모드로 만든다
wlan.active(True)                               # 무선 안테나를 켠다

print("주변 와이파이를 찾는 중... (몇 초 걸립니다)")
found = wlan.scan()                             # 결과: (이름, 주소, 채널, 신호, 보안, 숨김)
found.sort(key=lambda w: w[3], reverse=True)    # 신호가 센 순서로 (0 에 가까울수록 셈)
AUTH = ["열림", "WEP", "WPA", "WPA2", "WPA/WPA2", "WPA2-기업", "WPA3", "WPA2/3"]

for ssid, bssid, channel, rssi, auth, hidden in found:
    if found:
        best_wifi = found[0]
        try:
            name = best_wifi[0].decode() or "(숨김)"
        except UnicodeError:                        # 옛 공유기의 특수한 이름은 글자로 못 바꾼다
            name = "(읽을 수 없는 이름)"
        kind = AUTH[auth] if auth < len(AUTH) else str(auth) 
        print("가장 신호가 센 와이파이: ", name)
        break
    else:
        print("찾은 와이파이가 없습니다")
                                              #s : string(문자), d : decimal(숫자)

print("총", len(found), "개를 찾았습니다")
wlan.active(False)

# ⭐ 도전: 신호가 가장 센 와이파이 이름만 한 줄로 찍어 보자. (힌트: found[0])
# for문 사용하여 만들기
