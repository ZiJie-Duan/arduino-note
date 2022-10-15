from linkkit import linkkit
import time

class tests:

    def __init__(self):
        self.__lk = linkkit.LinkKit(
        host_name="cn-shanghai",
        product_key="a1OgKq4TEdh",
        device_name="Peter_beijing_pc",
        device_secret="65003893c41a7fbb38b8f0366f3a97fc")
        self.__lk.thing_setup(r"C:\Users\lucyc\Desktop\pc_controler\tsl.json")

        self.__lk.on_thing_disable = self.on_thing_disable
        self.__lk.on_thing_enable = self.on_thing_enable
        self.__lk.on_connect = self.on_connect
        self.__lk.on_disconnect = self.on_disconnect
        self.__lk.on_thing_prop_post = self.on_thing_prop_post
        self.__lk.on_thing_prop_changed = self.on_thing_prop_changed
        self.__lk.connect_async()

    def on_thing_enable(self, userdata):
        print("on_thing_enable")

    def on_thing_disable(self, userdata):
        print("on_thing_disable")

    def on_connect(session_flag, rc, userdata):
        print("on_connect:%d,rc:%d,userdata:" % (session_flag, rc))
        pass

    def on_disconnect(rc, userdata):
        print("on_disconnect:rc:%d,userdata:" % rc)

    def on_thing_prop_post(self, request_id, code, data, message,userdata):
        print("on_thing_prop_post request id:%s, code:%d, data:%s message:%s" %
            (request_id, code, str(data), message))

    def on_thing_prop_changed(self, params, userdata):
        print("on_thing_prop_changed params:" + str(params))

    def upload(self,state):
        data = {
            "computer_state": int(state)
        }
        rc, request_id = self.__lk.thing_post_property(data)

a = tests()
while True:
    b = input(">>")
    a.upload(b)
