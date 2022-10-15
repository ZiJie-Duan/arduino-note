import network
import socket
import time
from machine import Pin

Buzzer_pin = Pin(4, Pin.OUT)
Fire_pin = Pin(5, Pin.OUT)
Light_pin = Pin(16, Pin.OUT)
Buzzer_pin.on()


def do_connect():
    wlan = network.WLAN(network.STA_IF) # create station interface
    wlan.active(True)       # activate the interface
    wlan.scan()             # scan for access points
    wlan.connect('S', '9123456789') # connect to an AP


def get_fire_command():
    host = "192.168.0.11"
    port = 24680
    sock = socket.socket()
    sock.settimeout(5)
    sock.connect((host, port))
    data = "Fire_Waiting..."
    sock.send(data.encode("utf-8"))
    server_rec = sock.recv(1024).decode("utf-8")
    sock.close()
    if server_rec == "Fire":
        return True
    else:
        return False

def fire_reminder():
    print("sss")
    global Buzzer_pin
    time_interval = 0.5
    while time_interval>0.1:
        time.sleep(time_interval)
        Light_pin.on()
        Buzzer_pin.off()
        time.sleep(time_interval)
        Light_pin.off()
        Buzzer_pin.on()
        time_interval = time_interval - 0.03
    print("msss")
    Light_pin.on()
    Buzzer_pin.off()
    time.sleep(1)
    Light_pin.off()
    Buzzer_pin.on()
    print("ok")

def fire():
    global Fire_pin
    Fire_pin.on()
    time.sleep(1)
    Fire_pin.off()

def light_flash():
    Light_pin.on()
    time.sleep(0.2)
    Light_pin.off()

def main():
    js = 0
    while True:
        light_flash()
        print("START")
        try:
            if get_fire_command():
                print("fire !")
                fire_reminder()
                fire()
                time.sleep(2)
            else:
                time.sleep(2)
                print("still waiting")
        except Exception as e:
            print("CORE-ERROW")
            print(e)
            time.sleep(5)
            js += 1
            if js > 5:
                print("stop program")
                break
do_connect()
main()