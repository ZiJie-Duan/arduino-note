import json
import time

class APP():
    def __init__(self):
        self.esp_machine = None

    def start(self):
        img1 = []
        with open("/apps/Little_Dinosaur/running1.json") as zx:
            img1 = json.load(zx)
        img2 = []
        with open("/apps/Little_Dinosaur/running2.json") as zx:
            img2 = json.load(zx)
        img3 = []
        with open("/apps/Little_Dinosaur/fast_runing1.json") as zx:
            img3 = json.load(zx)
        img4 = []
        with open("/apps/Little_Dinosaur/fast_runing2.json") as zx:
            img4 = json.load(zx)
        

        action_state = 0
        while True:
            state, value = self.esp_machine.get_gpio_change()
            if state:
                if value == "in":
                    pass
                if value == "select":
                    pass
                if value == "out":
                    break
                time.sleep(0.2)
                
            if action_state == 0:
                action_state = 1
                self.esp_machine.oled1.fill(0)
                for pix in img1:
                    self.esp_machine.oled1.pixel(pix[0], pix[1], 1)
                self.esp_machine.oled1.show()

                self.esp_machine.oled2.fill(0)
                for pix in img4:
                    self.esp_machine.oled2.pixel(pix[0], pix[1], 1)
                self.esp_machine.oled2.show()
            else:
                action_state = 0
                self.esp_machine.oled1.fill(0)
                for pix in img2:
                    self.esp_machine.oled1.pixel(pix[0], pix[1], 1)
                self.esp_machine.oled1.show()

                self.esp_machine.oled2.fill(0)
                for pix in img3:
                    self.esp_machine.oled2.pixel(pix[0], pix[1], 1)
                self.esp_machine.oled2.show()
        
