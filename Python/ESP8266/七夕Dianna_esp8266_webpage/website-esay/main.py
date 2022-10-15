import time
import network
try:
    import usocket as socket
except:
    import socket


class SocketDrive:

    def __init__(self):
        self.ap = network.WLAN(network.AP_IF) # create access-point interface
        self.ap.active(True)         # activate the interface
        self.ap.config(essid='Dianna-ESP-QIXI') # set the ESSID of the access point
        self.ap.ifconfig(('192.168.0.1', '255.255.255.0', '192.168.0.1', '208.67.222.222'))
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 设置当服务器先close 即服务器端4次挥手之后资源能够立即释放，这样就保证了，下次运行程序时 可以立即绑定7788端口
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # 设置服务端提供服务的端口号
        self.server_socket.bind(('', 80))
        # 使用socket创建的套接字默认的属性是主动的，使用listen将其改为被动，用来监听连接
        self.server_socket.listen(1) #最多可以监听128个连接

    def send_back_website(self):
        client_socket, _ = self.server_socket.accept()
        _ = client_socket.recv(1024).decode("utf-8") #  1024表示本次接收的最大字节数
        # 打印从客户端发送过来的数据内容

        f = open("index.html")
        js = 0
        while True:
            response = f.read(10240)
            if response:
                client_socket.sendall(response)
                js += 1
                print("send" + str(js))
            else:
                break
        f.close()
        client_socket.close() 
        print("finish to sent!")


def main():
    s = SocketDrive()
    while True:
        try:
            s.send_back_website()
        except OSError:
            print("连接器发生设备断联错误-进行重置")

if __name__ == "__main__":
    main()


