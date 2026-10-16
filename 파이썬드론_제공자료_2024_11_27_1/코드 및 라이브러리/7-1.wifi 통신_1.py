print("Scanning for WiFi networks, please wait...")
print("")

import network
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)

authmodes = ['Open', 'WEP', 'WPA-PSK', 'WPA2-PSK', 'WPA/WPA2-PSK']

for (ssid, bssid, channel, RSSI, authmode, hidden) in sta_if.scan():
    print("* {:s}".format(ssid))
    if 0 <= authmode < len(authmodes):
        auth_desc = authmodes[authmode]
    else:
        auth_desc = "Unknown"

    print("   - Auth: {} {}".format(auth_desc, '(hidden)' if hidden else ''))
    print("   - Channel: {}".format(channel))
    print("   - RSSI: {}".format(RSSI))
    print("   - BSSID: {:02x}:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}".format(*bssid))
    print()