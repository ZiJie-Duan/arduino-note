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

    def on_disconnect(rc, userdata):
        print("on_disconnect:rc:%d,userdata:" % rc)

    def on_thing_enable(self, userdata):
        print("on_thing_enable")

    def on_thing_disable(self, userdata):
        print("on_thing_disable")

    def on_thing_prop_post(self, request_id, code, data, message,userdata):
        print("on_thing_prop_post request id:%s, code:%d, data:%s message:%s" %
            (request_id, code, str(data), message))

    def on_thing_prop_changed(self, params, userdata):
        #阿里云IOT平台进行 属性下发时的调用
        print("on_thing_prop_changed params:" + str(params))
        if "Frp_Server_IP" in params:
            print("{} 进行重设至 {}".format("Frp_Server_IP",params["Frp_Server_IP"]))
            self.windows.datas["common"]["server_addr"] = params["Frp_Server_IP"]
            self.windows.write_frp_ini()

        if "Frp_Running_State" in params:
            if params["Frp_Running_State"] == 1:
                print("{} 进行重设至 {}".format("Frp_Running_State",params["Frp_Running_State"]))
                self.windows.running_state = 1
                self.windows.start_frp_father()
            else:
                print("{} 进行重设至 {}".format("Frp_Running_State",params["Frp_Running_State"]))
                self.windows.running_state = 0

    def upload_state(self):
        prop_data = {}
        prop_data["Frp_Running_State"] = self.windows.running_state
        prop_data["Frp_Server_IP"] = self.windows.datas["common"]["server_addr"]

        rc, request_id = self.lk.thing_post_property(prop_data)

def main():
    iot = IOT(windows=WINDOWS_CONTROL())
    while 1:
        time.sleep(3)
        iot.upload_state()

main()