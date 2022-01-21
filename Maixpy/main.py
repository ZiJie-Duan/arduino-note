import sensor, lcd
import time
from Maix import I2S
import time
import uos

def main():
    lcd.init()
    #sensor.reset(freq=24000000)
    sensor.set_auto_gain(1)
    sensor.set_hmirror(0)
    sensor.set_vflip(1)
    sensor.set_pixformat(sensor.RGB565)
    sensor.set_framesize(sensor.QVGA)
    sensor.run(1)

    for x in range(50):
        for i in range(15):
            img = sensor.snapshot()
            img_show = img.copy()
            img_show = img_show.draw_rectangle(48, 7, 225, 225)
            img_show = img_show.draw_string(100, 100, "Take Photo {}".format(i), color=(255,51,51), scale=1.5)
            lcd.display(img_show)
        img = sensor.snapshot()
        img_save = img.copy(roi=(48, 7, 225, 225))
        lcd.display(img_save)
        img.save("/sd/{}.jpg".format(str(x)), quality=99)
        time.sleep(1)
main()



'''
try:
    main()
    pass
except Exception as e:
    lcd.init()
    lcd.draw_string(10, 10, "program err: {}".format(str(e)), lcd.RED, lcd.BLACK)
    print(e)



js = 50
while True:
    img = sensor.snapshot()
    img.draw_string(100, 100, "Take Photo {}".format(js), color=(255,51,51), scale=1.5)
    lcd.display(img)
    js -= 1
    if js < 1:
       img = sensor.snapshot()
       for i in range(10):
           img_or = img.copy()
           img_or.draw_string(5, 5, str(10-i), color=(255,51,51), scale=1)
           lcd.display(img_or)
           time.sleep(1)
       js = 50
       files = uos.ilistdir()
       for x in range(9999):
           if str(x) not in files:
               img.save("/sd/{}.jpg".format(str(x)), quality=95)
               break


lcd.draw_string(100, 100, "Take Photo {}".format(3-js2), lcd.RED, lcd.BLACK)
class SCREEN():
    def __init__(self,lcd):
        lcd = lcd
        lcd.init()

    def show_text(self,text,mode="normal"):
        if mode == "normal":
            text_list = text.split(" ")
            sentence_list = []
            sentence = ""
            singel_letter = 0
            for word in text_list:
                singel_letter += len(word) + 1
                if singel_letter < 30:
                    sentence = sentence +  word + " "
                    print(sentence)
                else:
                    sentence_list.append(sentence)
                    print(sentence)
                    print(sentence_list)
                    singel_letter = 0
                    sentence = ""
                    sentence = sentence +  word + " "

            line = 0
            for sentence in sentence_list:
                print("sentence : {}".format(sentence))
                self.lcd.draw_string(5, 5+line, sentence, lcd.RED, lcd.BLACK)
                line += 10

'''
