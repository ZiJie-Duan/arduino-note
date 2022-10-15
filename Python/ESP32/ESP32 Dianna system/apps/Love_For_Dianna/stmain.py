import json
import time

class APP():
    def __init__(self):
        self.esp_machine = None

    def start(self):
        img = []
        with open("/apps/Love_For_Dianna/heart.json") as zx:
            img = json.load(zx)
            self.esp_machine.oled1.fill(0)
            for pix in img:
                self.esp_machine.oled1.pixel(pix[0], pix[1], 1)
            self.esp_machine.oled1.show()
        
        message = "I Love You Dianna! Merry Christmas!"
        self.esp_machine.show_text(text=message,screen_list=[2],center=True)
        
        oled_invert = 1
        heart_beat = 0
        while True:
            state, value = self.esp_machine.get_gpio_change()
            if state:
                if value == "in":
                    pass
                if value == "select":
                    self.esp_machine.oled1.fill(0)
                    if oled_invert == 1:
                        oled_invert = 2
                    else:
                        oled_invert = 1
                    self.esp_machine.oled1.invert(oled_invert)
                    for pix in img:
                        self.esp_machine.oled1.pixel(pix[0], pix[1], 1)
                    self.esp_machine.oled1.show()
                if value == "out":
                    break
                time.sleep(0.2)
