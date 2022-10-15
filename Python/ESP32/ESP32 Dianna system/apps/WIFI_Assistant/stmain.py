import json
import time

class APP():
    def __init__(self):
        self.esp_machine = None
        self.wifi_name = ""
        self.wifi_password = ""
        self.wifi_config = {}

    def read_wifi_config(self):
        with open("/apps/WIFI_Assistant/wifi.json") as zx:
            self.wifi_config = json.load(zx)

    def start(self):        
        message = "Wifi Assistant. This program can help you to connect your wifi and start webrepl."
        self.esp_machine.show_text(text=message,screen_list=[2],center=True)
        self.read_wifi_config()
        time.sleep(0.5)

        while True:
            state, value = self.esp_machine.get_gpio_change()
            if state:
                if value == "in":
                    message = "Wifi Assistant. Please choose your Wifi. Press Green to confirm."
                    self.esp_machine.show_text(text=message,screen_list=[2],center=True)
                    break
                if value == "select":
                    pass
                if value == "out":
                    return None
                time.sleep(0.2)

        wifi_index = 1
        wifi_name = self.wifi_config[str(wifi_index)]["name"]
        message_wifi = "Wifi Name: {}".format(wifi_name)
        self.esp_machine.show_text(text=message_wifi,screen_list=[1],center=True)
        time.sleep(0.5)

        while True:
            state, value = self.esp_machine.get_gpio_change()
            if state:
                if value == "in":
                    break
                if value == "select":
                    wifi_index += 1
                    if wifi_index <= len(self.wifi_config):
                        pass
                    else:
                        wifi_index = 1
                    wifi_name = self.wifi_config[str(wifi_index)]["name"]
                    message_wifi = "Wifi Name: {}".format(wifi_name)
                    self.esp_machine.show_text(text=message_wifi,screen_list=[1],center=True)

                if value == "out":
                    return None
                time.sleep(0.2)

        message_wifi = "Wifi Assistant. START TO CONNECT WIFI!"
        self.esp_machine.show_text(text=message_wifi,screen_list=[2],center=True)

        wifi_name = self.wifi_config[str(wifi_index)]["name"]
        wifi_password = self.wifi_config[str(wifi_index)]["password"]
        time.sleep(1.5)
        self.esp_machine.start_wifi(name=wifi_name,password=wifi_password)

        if self.esp_machine.test_wifi_link():
            message_wifi = "Wifi Assistant. CONNECT WIFI SUCCESS!"
            self.esp_machine.show_text(text=message_wifi,screen_list=[2],center=True)
            time.sleep(2)

            self.esp_machine.start_webrepl(password="1111")

            message_wifi = "Wifi Assistant. webrepl START! Now you can shutdown your Dianna System"
            self.esp_machine.show_text(text=message_wifi,screen_list=[2],center=True)

            ip,_,_,_ = self.esp_machine.wlan.ifconfig()
            message_wifi = "IP: {} Webrepl_password: {}".format(ip,"1111")
            self.esp_machine.show_text(text=message_wifi,screen_list=[1],center=True)
            
        else:
            message_wifi = "Wifi Assistant. CONNECT WIFI FAIL! Program auto stop!"
            self.esp_machine.show_text(text=message_wifi,screen_list=[2],center=True)
        
        while True:
            state, value = self.esp_machine.get_gpio_change()
            if state:
                if value == "in":
                    break
                if value == "select":
                    pass
                if value == "out":
                    break
                time.sleep(0.2)

