import socket


def heart_listen():

    host = "0.0.0.0"
    port = 2333
    sock = socket.socket()
    sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    sock.bind((host, port))
    sock.listen(5)
    while True:
        cli, _ = sock.accept()
        data = cli.recv(1024).decode()
        print(data)
        send = input(">>")
        cli.send(send.encode("utf-8"))
        print("\nOver\n")
heart_listen()