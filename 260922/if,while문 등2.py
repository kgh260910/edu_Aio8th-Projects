from machine import Pin
flash = Pin(4, Pin.OUT, value=0)
if flash.value() == 1:
    print("플래시 켜짐")
else:
    print("플래시 꺼짐")
    