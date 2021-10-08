from linkkit import linkkit
import time
import configparser
import os
import threading
import os
import psutil

class WINDOWS_CONTROL:
    def __init__(self):
        self.datas = {
            "common":{
                "server_addr" : "0.0.0.0",
                "server_port" : "3112",
                "token" : "PeterIsTheGod"
            },
            "rdp":{
                "type" : "tcp",
                "local_ip" : "127.0.0.1",
                "local_port" : "3389",
                "remote_port" : "7001"
            }
        }
        self.running_state = 0
    
    def get_data(self):
        config = configparser.ConfigParser()
        config.read(r'C:\Users\lucyc\Desktop\frp_0.37.1_windows_amd64\frpc.ini')
        values = config.items('common')
        for key, value in values:
            self.datas["common"][key]=value

    def kill_program(self):
        try:
            pids = psutil.pids()
            for pid in pids:
                p = psutil.Process(pid)
                # print('pid-%s,pname-%s' % (pid, p.name()))
                if p.name() == 'frpc.exe':
                    cmd = 'taskkill /F /IM frpc.exe'
                    os.system(cmd)
        except:
            pass

    def write_frp_ini(self):
        config = configparser.ConfigParser()
        for section, data in self.datas.items():
            config.add_section(section)
            for key, value in data.items():
                config.set(section, key, value)
        config.write(open(r'C:\Users\lucyc\Desktop\frp_0.37.1_windows_amd64\frpc.ini', "w"))

    def start_frp_small_son(self):
        os.system(r"C:\Users\lucyc\Desktop\frp_0.37.1_windows_amd64\frpc.exe -c C:\Users\lucyc\Desktop\frp_0.37.1_windows_amd64\frpc.ini")

    def start_frp(self):
        ts = threading.Thread(target=self.start_frp_small_son)
        ts.setDaemon(True)
        ts.start()
        while True:
            if self.running_state == 0:
                time.sleep(1)
                self.kill_program()
                print("frp 服务退出")
                break

    def start_frp_father(self):
        t = threading.Thread(target=self.start_frp)
        t.start()
    
    def Shut_Down(self):
        os.system("shutdown -s -f -t 0")

    def command(self,params):
        if "Frp_Server_IP" in params:
            print("{} 进行重设至 {}".format("Frp_Server_IP",params["Frp_Server_IP"]))
            self.datas["common"]["server_addr"] = params["Frp_Server_IP"]
            self.write_frp_ini()
            print("Finish")
        
        if "Frp_Server_Port" in params:
            print("{} 进行重设至 {}".format("Frp_Server_Port",params["Frp_Server_Port"]))
            self.datas["common"]["server_port"] = params["Frp_Server_Port"]
            self.write_frp_ini()
        
        if "Frp_Server_Token" in params:
            print("{} 进行重设至 {}".format("Frp_Server_Token",params["Frp_Server_Token"]))
            self.datas["common"]["token"] = params["Frp_Server_Token"]
            self.write_frp_ini()

        if "Frp_Running_Switch" in params:
            if params["Frp_Running_Switch"] == 1:
                print("{} 进行重设至 {}".format("Frp_Running_Switch",params["Frp_Running_Switch"]))
                self.running_state = 1
                self.start_frp_father()
            else:
                print("{} 进行重设至 {}".format("Frp_Running_Switch",params["Frp_Running_Switch"]))
                self.running_state = 0
        
        if "PC_Power" in params:
            if params["PC_Power"] == 0:
                self.Shut_Down()
    
    def prepare_data(self):
        prop_data = {}
        prop_data["Frp_Running_Switch"] = self.running_state
        prop_data["Frp_Server_IP"] = self.datas["common"]["server_addr"]
        prop_data["Frp_Server_Port"] = self.datas["common"]["server_port"]
        prop_data["Frp_Server_Token"] = self.datas["common"]["token"]
        prop_data["PC_Power"] = 1
        return prop_data

class IOT:

    def __init__(self,windows):
        self.windows = windows
        self.lk = linkkit.LinkKit(
            host_name="cn-shanghai",
            product_key="a1OgKq4TEdh",
            device_name="Peter_beijing_pc",
            device_secret="65003893c41a7fbb38b8f0366f3a97fc")          
        # lk.config_mqtt(endpoint="iot-cn-6ja******.mqtt.iothub.aliyuncs.com")
        self.lk.config_mqtt(port=1883, protocol="MQTTv311", transport="TCP",
                    secure="TLS", keep_alive=60, clean_session=True,
                    max_inflight_message=20, max_queued_message=0,
                    auto_reconnect_min_sec=1,
                    auto_reconnect_max_sec=60,
                    cadata=None)

        self.lk.thing_setup(r"C:\Users\lucyc\Desktop\arduino-note\IOT_FRP_Remote_Control\tsl.json")
        self.lk.on_connect = self.on_connect
        self.lk.on_disconnect = self.on_disconnect
        self.lk.on_thing_enable = self.on_thing_enable
        self.lk.on_thing_disable = self.on_thing_disable
        self.lk.on_thing_prop_post = self.on_thing_prop_post
        self.lk.on_thing_prop_changed = self.on_thing_prop_changed
        self.lk.connect_async()

    
    def on_connect(session_flag, rc, userdata):
        print("on_connect:%d,rc:%d,userdata:" % (session_flag, rc))
        pass

    def on_disconnect(self, rc, userdata):
        print("on_disconnect:rc:%d,userdata:" % rc)
        self.windows.Shut_Down()

    def on_thing_enable(self, userdata):
        print("on_thing_enable")

    def on_thing_disable(self, userdata):
        print("on_thing_disable")
        self.windows.Shut_Down()

    def on_thing_prop_post(self, request_id, code, data, message,userdata):
        print("on_thing_prop_post request id:%s, code:%d, data:%s message:%s" %
            (request_id, code, str(data), message))

    def on_thing_prop_changed(self, params, userdata):
        #阿里云IOT平台进行 属性下发时的调用s
        print("on_thing_prop_changed params:" + str(params))
        self.windows.command(params=params)

    def upload_state(self):
        prop_data = self.windows.prepare_data()
        rc, request_id = self.lk.thing_post_property(prop_data)

def main():
    windows = WINDOWS_CONTROL()
    windows.get_data()
    iot = IOT(windows=windows)
    while 1:
        time.sleep(20)
        iot.upload_state()


main()
