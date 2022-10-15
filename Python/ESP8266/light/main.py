import network
import socket
import time
from machine import Pin

light_state = False
lock_state = False
MACHINE_ID = "LIGHT-PETER-ROOM"

light_pin = Pin(4, Pin.OUT)
touch_pin = Pin(5, Pin.IN)


def update_light_state():
    global light_state, lock_state, light_pin, touch_pin
    try:
        host = "192.168.0.11"
        port = 24680
        sock = socket.socket()
        sock.settimeout(5)
        sock.connect((host, port))
        data = "machine@" + MACHINE_ID
        sock.send(data.encode("utf-8"))
        server_rec = sock.recv(1024).decode("utf-8")
        sock.close()
    except:
        server_rec = "ULOCK"

    if server_rec == "OPEN":
        light_state = True
        light_pin.on()
    if server_rec == "CLOSE":
        light_state = False
        light_pin.off()
    if server_rec == "LOCK":
        lock_state = True
    if server_rec == "ULOCK":
        lock_state = False
    if server_rec == "NONE":
        pass
    

def test_bottom():
    global light_state, touch_pin
    if touch_pin.value() == 1:
        print("change state")
        if lock_state == False:
            if light_state == True:
                light_state = False
                light_pin.off()
            else:
                light_state = True
                light_pin.on()
        time.sleep(0.3)



print("start")
while True:
    try:
        for x in range(1000):
            test_bottom()
        update_light_state()
    except Exception as e:
        print(e)
        time.sleep(5)