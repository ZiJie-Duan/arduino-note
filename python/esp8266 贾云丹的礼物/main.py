from machine import Pin, I2C
import time
from ssd1306 import SSD1306_I2C
import network
from socket import *
import json



class MessageControl:

    def __init__(self):
        self.file_name = "data.json"
        self.message_list = [["Dianna"]]
    
    def load_message(self):
        with open(self.file_name) as zx:
            self.message_list = json.load(zx)

    def save_message(self):
        with open(self.file_name, 'w') as zx:
            zx.write(json.dumps(self.message_list))
    
    def add_message(self,messages):

        if messages in self.message_list:
            pass
        else:
            self.message_list.append(messages)
    
    def del_message(self,messages):
        self.message_list.remove(messages)

    def del_all_message(self):
        self.message_list = [["Dianna"]]

    def get_all_messages(self):
        return self.message_list

    


class OledDrive:
    
    def __init__(self):
        self.i2c = I2C(scl=Pin(5), sda=Pin(4))
        self.oled = SSD1306_I2C(128, 64, self.i2c)

    def show_small(self):
        img_names = [1,2,3,4,5,6,7,8,9,10]
        img = []
        while True:
            for img_name in img_names:
                with open(str(img_name)+".json") as zx:
                    img = json.load(zx)
                self.oled.fill(0)
                for pix in img:
                    self.oled.pixel(pix[0], pix[1], 1)
                self.oled.show()
                img = []

    def change_message(self,messages):
        self.oled.fill(0)
        line = 0
        for message in messages:
            print("change_oled_to " + message)
            self.oled.text(message, 0, line)
            line += 10
            if line > 60:
                break
        self.oled.show()

    def show(self):
        self.oled.show()

    def white(self):
        self.oled.fill(1)
        self.oled.show()
    
    def black(self):
        self.oled.fill(0)
        self.oled.show()

    def show_system_page(self):
        self.oled.fill(0)
        self.oled.text("Dianna", 0, 0)
        self.oled.text("System V1.0", 0, 10)
        self.oled.text("ROOT MOD", 0, 20)
        self.oled.text("made by Peter", 0, 30)
        self.oled.show()
    
    def show_opening_page(self):
        self.oled.fill(0)
        self.oled.text("Dianna", 35, 30)
        self.oled.show()


class SocketDrive:

    def __init__(self):
        self.ap = network.WLAN(network.AP_IF) # create access-point interface
        self.ap.active(True)         # activate the interface
        self.ap.config(essid='Dianna-ESP',password="diannapeter") # set the ESSID of the access point
        self.ap.ifconfig(('192.168.0.1', '255.255.255.0', '192.168.0.1', '208.67.222.222'))
        # 创建套接字
        self.server_socket = socket(AF_INET, SOCK_STREAM)
        # 设置当服务器先close 即服务器端4次挥手之后资源能够立即释放，这样就保证了，下次运行程序时 可以立即绑定7788端口
        self.server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        # 设置服务端提供服务的端口号
        self.server_socket.bind(('', 80))
        # 使用socket创建的套接字默认的属性是主动的，使用listen将其改为被动，用来监听连接
        self.server_socket.listen(128) #最多可以监听128个连接
        # 开启while循环处理访问过来的请求 

    def message_update(self):
        """为一个客户端服务"""
        # 接收对方发送的数据
        client_socket, clientAddr = self.server_socket.accept()
        recv_data = client_socket.recv(1024).decode("utf-8") #  1024表示本次接收的最大字节数
        # 打印从客户端发送过来的数据内容
        #print("client_recv:",recv_data)
        recv_data = recv_data.split("\n")

        messages = []
        lines = []
        data=""
        if "GET /?data=" in recv_data[0]:
            data = recv_data[0][11:-9]
            lines = data.split("@")
            for line in lines:
                messages.append(" ".join(line.split("%20")))

        client_socket.send("copy that!".encode("utf-8"))   #转码utf-8并send数据到浏览器
        client_socket.close()

        if messages == []:
            return None
        else:
            return messages
    

class Core:

    def __init__(self, message_control, oled_drive, socket_drive):
        self.messagec = message_control
        self.oled = oled_drive
        self.socket = socket_drive
        self.system_pin = Pin(13, Pin.IN, Pin.PULL_UP)
        self.buttom_pin = Pin(12, Pin.IN)


    def is_system_run(self):
        for x in range(100):
            if self.system_pin.value() == 0:
                print("prepare into system control")
                time.sleep(1)
                if self.system_pin.value() == 0:
                    return True
        return False

    
    def sys_mod(self):
        self.oled.show_system_page()
        while True:
            messages = self.socket.message_update()
            if messages == ["save "]:
                self.messagec.save_message()
                self.oled.change_message(messages=["Save Finish"])

            elif messages == ["show "]:
                message_list = self.messagec.get_all_messages()
                print(message_list)
                for messagepage in message_list:
                    self.oled.change_message(messages=messagepage)
                    time.sleep(1)

            elif messages == ["del "]:
                self.messagec.del_all_message()
                self.oled.change_message(messages=["Delet Finish"])

            elif messages == ["quit "]:
                break

            elif messages != None:
                self.messagec.add_message(messages=messages)
                self.oled.change_message(messages=messages)


    def buttom_is_put(self):
        if self.buttom_pin.value() == 1:
            time.sleep(0.2)
            if self.buttom_pin.value() == 1:
                return True
        return False


    def start(self):
        
        if self.is_system_run():
            if self.buttom_is_put():
                self.oled.show_small()
            self.sys_mod()

        self.oled.show_opening_page()
        message_index = 0

        while True:
            time.sleep(0.1)
            if self.buttom_is_put():
                message_page = self.messagec.message_list[message_index]
                self.oled.change_message(messages=message_page)
                if message_index == len(self.messagec.message_list)-1:
                    message_index = 0
                else:
                    message_index += 1



def main():
    oled_drive = OledDrive()
    message_control = MessageControl()
    message_control.load_message()
    socket_drive = SocketDrive()
    core = Core(message_control=message_control, oled_drive=oled_drive, socket_drive=socket_drive)
    core.start()



if __name__ == "__main__":
    main()


