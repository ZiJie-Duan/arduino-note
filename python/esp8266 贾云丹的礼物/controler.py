import socket

host = "192.168.0.1"
port = 80
sock = socket.socket()
sock.connect((host, port))
sock.send("hello@second line".encode("utf-8"))
server_rec = sock.recv(1024).decode("utf-8")
sock.close()
print(server_rec)
