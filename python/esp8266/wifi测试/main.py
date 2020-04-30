import network
import socket
import time
from machine import Pin


p1 = Pin(1, Pin.OUT)
p2 = Pin(2, Pin.OUT)
p3 = Pin(3, Pin.OUT)
p4 = Pin(4, Pin.OUT)


def do_connect():
    wlan = network.WLAN(network.STA_IF) # create station interface
    wlan.active(True)       # activate the interface
    wlan.scan()             # scan for access points
    wlan.connect('S', '9123456789') # connect to an AP

def set_pin(server_rec):
    global p1, p2, p3, p4
    if server_rec[0] == "1":
        print("yes")
        if server_rec[1] == "h":
            p1.on()
            print("yes")
        else:
            p1.off()
            print("no")

    elif server_rec[0] == "2":
        if server_rec[1] == "h":
            p2.on()
        else:
            p2.off()

    elif server_rec[0] == "3":
        if server_rec[1] == "h":
            p3.on()
        else:
            p3.off()

    elif server_rec[0] == "4":
        if server_rec[1] == "h":
            p4.on()
        else:
            p4.off()

def send_heart():
    host = "192.168.0.11"
    port = 2333
    sock = socket.socket()
    sock.connect((host, port))
    sock.send("hello".encode("utf-8"))
    server_rec = sock.recv(1024).decode("utf-8")
    sock.close()
    print(server_rec)
    server_rec = server_rec.split("@")
    print(server_rec)
    set_pin(server_rec)
    print(server_rec)


while True:
    print("start")
    try:
        send_heart()
        time.sleep(5)
    except Exception as e:
        print(e)
        time.sleep(5)

