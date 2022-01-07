from machine import Pin


buttom_up = Pin(36, Pin.IN)
buttom_down = Pin(39, Pin.IN)
buttom_left = Pin(34, Pin.IN)
buttom_right = Pin(35, Pin.IN)
buttom_mid = Pin(27, Pin.IN)
buttom_a = Pin(25, Pin.IN)
buttom_b = Pin(26, Pin.IN)
buttom_c = Pin(23, Pin.IN)
buttom_d = Pin(22, Pin.IN)
while True:
    if buttom_up.value():
        print("up")
    if buttom_down.value():
        print("down")
    if buttom_left.value():
        print("left")
    if buttom_right.value():
        print("right")
    if buttom_mid.value():
        print("mid")
    if buttom_a.value():
        print("a")
    if buttom_b.value():
        print("b")
    if buttom_c.value():
        print("c")
    if buttom_d.value():
        print("d")