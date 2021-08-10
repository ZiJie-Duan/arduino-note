import socket

class ev3_linux_drive():

    def __init__(self):

    def stop_apache_server(self):
        os.system("service apache2 stop")

    def start_apache_server(self):
        os.system("service apache2 start")

class socket_drive():

    def __init__(self):
        self.sk = socket.socket() # 默认使用IPV4和TCP
        self.sk.bind(('127.0.0.1',2122))
        self.sk.listen(1)

    def listing(self):
        cli, _ = sk.accept()
        





'''
def heart_beat_core():
    host = "127.0.0.1"
    port = 2122
    sock = socket.socket()
    sock.settimeout(1)
    sock.connect((host, port))
    sock.sendall("test_message".encode("utf-8"))

    server_rec = sock.recv(10240).decode("utf-8")
    print(server_rec)
    sock.close()

heart_beat_core()
'''