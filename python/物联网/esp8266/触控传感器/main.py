import socket
import time
from machine import Pin

light = Pin(4, Pin.OUT)

def disco():
    time.sleep()
    light.off()
    light.on()
def control_the_light(server_rec):
    if server_rec[0] == "1":
        if server_rec[1] == "0":
            print("0")
            light.off()
        if server_rec[1] == "1":
            print("1")
            light.on()
        if server_rec[1] == "3":
            light.on()
            time.sleep(1)     
            light.off()  # sleep for 10 microseconds
            for _ in range(50):
                light.on()
                time.sleep(0.2)    
                light.off()  
                time.sleep(0.3)
                print("FINISH")

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
    control_the_light(server_rec)
    print(server_rec)


while True:
    try:
        send_heart()
        time.sleep(5)

    except Exception as e:
        print(e)
        time.sleep(5)




