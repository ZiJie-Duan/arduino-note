from linkkit import linkkit
import time
import os

class IOT:

    def __init__(self):
        self.lk = linkkit.LinkKit(
            host_name="cn-shanghai",
            product_key="a1OgKq4TEdh",
            device_name="Raspberry",
            device_secret="2d06b97b03b9073b9a796ccef8d1b489")          
        # lk.config_mqtt(endpoint="iot-cn-6ja******.mqtt.iothub.aliyuncs.com")
        self.lk.config_mqtt(port=1883, protocol="MQTTv311", transport="TCP",
                    secure="TLS", keep_alive=60, clean_session=True,
                    max_inflight_message=20, max_queued_message=0,
                    auto_reconnect_min_sec=1,
                    auto_reconnect_max_sec=60,
                    cadata=None)

        self.lk.thing_setup("tsl.json")
        self.lk.on_connect = self.on_connect
        self.lk.on_disconnect = self.on_disconnect
        self.lk.on_thing_enable = self.on_thing_enable
        self.lk.on_thing_disable = self.on_thing_disable
        self.lk.on_thing_prop_post = self.on_thing_prop_post
        self.lk.on_thing_prop_changed = self.on_thing_prop_changed
        self.lk.connect_async()
        self.pc_power = 0
    
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
        #阿里云IOT平台进行 属性下发时的调用s
        print("on_thing_prop_changed params:" + str(params))
        if "PC_Power" in params:
            if params["PC_Power"] == 1:
                print("唤醒PC主机")
                self.pc_power = 1
                os.system("etherwake 00:D8:61:77:C1:FC")
            else:
                print("关闭PC主机")
                self.pc_power = 0
                
    def upload_state(self):
        prop_data = {}
        prop_data["PC_Power"] = self.pc_power
        rc, request_id = self.lk.thing_post_property(prop_data)

def main():
    iot = IOT()
    while 1:
        time.sleep(20)
        iot.upload_state()

main()