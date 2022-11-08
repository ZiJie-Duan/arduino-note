from machine import Pin, I2C, freq
import time
import json
from ssd1306 import SSD1306_I2C
import _thread
import webrepl
import network

class ESP32_MACHINE:
    def __init__(self):
        self.buttom1 = None
        self.buttom2 = None
        self.buttom3 = None
        self.oled1 = None
        self.oled2 = None
        self.applist = []
        self.apps = []
        self.real_time_status = {
            "state" : False,
            "in":False,
            "select":False,
            "out":False
        }
        self.wlan = None
   
    def test_wifi_link(self):
        if self.wlan.isconnected():
            return True
        return False

    def start_wifi(self,name,password):
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        if self.test_wifi_link():
            pass
        else:
            try:
                self.wlan.connect(name, password)
            except:
                pass

    def start_webrepl(self,password):
        webrepl.start(password=password)

    def get_gpio_change(self):
        if self.real_time_status["state"]:
            # 检测到按键触动
            if self.real_time_status["select"]:
                return True, "select"
            if self.real_time_status["in"]:
                return True, "in"
            if self.real_time_status["out"]:  
                return True, "out"
            self.real_time_status["state"] = False
            return False, "None"
        else:
            return False, "None"
    
    def interactive_check(self):
        while True:
            if self.buttom1.value() == 1:
                self.real_time_status["in"] = True
                self.real_time_status["state"] = True
            else:
                self.real_time_status["in"] = False
            if self.buttom2.value() == 1: 
                self.real_time_status["select"] = True
                self.real_time_status["state"] = True
            else:
                self.real_time_status["select"] = False
            if self.buttom3.value() == 0:  #针对先行者开发板的 极端优化
                self.real_time_status["out"] = True
                self.real_time_status["state"] = True
            else:
                self.real_time_status["out"] = False

    def init_applist(self):
        with open("applist.json") as zx:
            self.applist = json.load(zx)
            for appName, appFile in self.applist.items():
                command = "import apps.{}.stmain".format(appFile)
                exec(command)
                app = "apps.{}.stmain".format(appFile)
                self.apps.append([appName,app])

    def pix_show(self,screen_list,pix_list):
        # 普通屏幕像素绘制，提供像素列表和显示屏幕列表作为参数
        if 1 in screen_list:
            self.oled1.fill(0)
            for pix in pix_list:
                self.oled1.pixel(pix[0], pix[1], 1)
            self.oled1.show()
        if 2 in screen_list:
            self.oled2.fill(0)
            for pix in pix_list:
                self.oled2.pixel(pix[0], pix[1], 1)
            self.oled2.show()
    
    def combine_pix_show(self,pix_list):
        # 合并屏幕像素绘制，提供像素列表，自动将屏幕合并显示
        self.oled1.fill(0)
        self.oled2.fill(0)
        for pix in pix_list:
            if pix[0] <= 128:
                self.oled1.pixel(pix[0], pix[1], 1)
            else:
                self.oled2.pixel(pix[0]-128, pix[1], 1)
        self.oled1.show()
        self.oled2.show()

    def close_screen(self,screen_list=[1,2]):
        if 1 in screen_list:
            self.oled1.fill(0)
            self.oled1.show()
        if 2 in screen_list:
            self.oled2.fill(0)
            self.oled2.show()

    def frame(self,screen_list,lenth=1):
        pixs = []
        y_axis_up = 0+lenth
        y_axis_down = 64-lenth
        for x_axis in range(0+lenth,128-lenth):
            pixs.append([x_axis,y_axis_up])
            pixs.append([x_axis,y_axis_down])

        x_axis_left = 0+lenth
        x_axis_right = 128-lenth
        for y_axis in range(0+lenth,64-lenth):
            pixs.append([x_axis_left,y_axis])
            pixs.append([x_axis_right,y_axis])

        if 1 in screen_list:
            self.oled1.fill(0)
            for pix in pixs:
                self.oled1.pixel(pix[0], pix[1], 1)
            self.oled1.show()
        if 2 in screen_list:
            self.oled2.fill(0)
            for pix in pixs:
                self.oled2.pixel(pix[0], pix[1], 1)
            self.oled2.show()
    
    def show_text(self,text,screen_list,center=False,str_lenth=0,screen_clean=True): 
        # str_lenth 字符串个数边界

        text_list = text.split(" ")
        data = []
        sentence = ""
        #循环自动按照空格分行
        for text in text_list:
            len_for_sentence = len(sentence+" "+text)
            max_lenth = 16 - str_lenth * 2
            if len_for_sentence < max_lenth:
                sentence += " " + text
            else:
                data.append(sentence)
                sentence = text
        data.append(sentence) # 加入列表末尾的一个 sentence
        data[0] = data[0][1:] # 去除因列表循环 不小心加入的空格

        if screen_clean:
            if 1 in screen_list:
                self.oled1.fill(0)
            if 2 in screen_list:  
                self.oled2.fill(0)

        if center:
            start_y_location = ((6-len(data))//2)*8
            if 1 in screen_list:
                for sentence in data:
                    start_x_location = (128-len(sentence*8))//2
                    self.oled1.text(sentence, start_x_location, start_y_location)
                    start_y_location += 10
                self.oled1.show()
            if 2 in screen_list:
                for sentence in data:
                    start_x_location = (128-len(sentence*8))//2
                    self.oled2.text(sentence, start_x_location, start_y_location)
                    start_y_location += 10
                self.oled2.show()  
        else:
            if 1 in screen_list:
                js = str_lenth*8
                for sentence in data:
                    self.oled1.text(sentence, str_lenth*8, js)
                    js += 10
                self.oled1.show()

            if 2 in screen_list:
                js = str_lenth*8
                for sentence in data:
                    self.oled2.text(sentence, str_lenth*8, js)
                    js += 10
                self.oled2.show()


class MICROPY_MACHINE(ESP32_MACHINE):
    def __init__(self) -> None:
        pass


class DIANNA_SYS:
    def __init__(self,esp_machine):
        self.esp_machine = esp_machine

    def show_logo(self):
        with open("logo.json") as zx:
            img = json.load(zx)
            self.esp_machine.pix_show(screen_list=[1],pix_list=img)
            self.esp_machine.frame(screen_list=[2],lenth=13)
            self.esp_machine.show_text(text="DIANNA SYSTEM V2.0",str_lenth=2,screen_list=[2],screen_clean=False,center=True)
        time.sleep(3)
        self.esp_machine.close_screen()
    
    def show_main_menu(self):
        self.esp_machine.init_applist()
        apps = self.esp_machine.apps
        selected_app = 0
        self.esp_machine.frame(screen_list=[1],lenth=8)
        self.esp_machine.show_text(text=apps[selected_app][0],str_lenth=2,screen_list=[1],screen_clean=False,center=True)
        intro = "Please select the app you want to use. Press the green button to enter."
        self.esp_machine.show_text(text=intro,screen_list=[2])
        while True:
            state, value = self.esp_machine.get_gpio_change()
            if state:
                if value == "select":
                    if selected_app+1 < len(apps):  
                        selected_app += 1
                    else:
                        selected_app = 0
                    self.esp_machine.frame(screen_list=[1],lenth=8)
                    self.esp_machine.show_text(text=apps[selected_app][0],\
                        str_lenth=2,screen_list=[1],screen_clean=False,center=True)
                if value == "in":
                    exec("appcore = {}.APP()".format(apps[selected_app][1]))
                    appcore.esp_machine = self.esp_machine
                    appcore.start()
                    self.esp_machine.frame(screen_list=[1],lenth=8)
                    self.esp_machine.show_text(text=apps[selected_app][0],str_lenth=2,screen_list=[1],screen_clean=False,center=True)
                    intro = "Please select the app you want to use. Press the green button to enter."
                    self.esp_machine.show_text(text=intro,screen_list=[2])
                if value == "out":
                    self.esp_machine.close_screen()
                    break
                time.sleep(0.2)



def main():
    esp_machine = ESP32_MACHINE()
    freq(240000000) 

    esp_machine.buttom1 = Pin(25, Pin.IN)
    esp_machine.buttom2 = Pin(26, Pin.IN)
    esp_machine.buttom3 = Pin(23, Pin.IN)

    i2c1 = I2C(scl=Pin(33), sda=Pin(32))
    oled1 = SSD1306_I2C(128, 64, i2c1)
    oled1.rotate(2)
    esp_machine.oled1 = oled1

    i2c2 = I2C(scl=Pin(13), sda=Pin(12))
    oled2 = SSD1306_I2C(128, 64, i2c2)
    oled2.rotate(2)
    esp_machine.oled2 = oled2

    dsg = DIANNA_SYS(esp_machine = esp_machine)
    dsg.show_logo()

    #_thread.start_new_thread(esp_machine.interactive_check, ())
    #dsg.show_main_menu()

if __name__ == "__main__":
    main()

