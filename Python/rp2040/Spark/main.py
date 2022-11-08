from machine import Pin, SoftI2C
import ssd1306
from time import sleep
import spark
import random

oled_width = 128
oled_height = 64
i2c = SoftI2C(scl=Pin(3), sda=Pin(2))
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

def say_hello():
    oled.fill(0)
    oled.invert(1)
    oled.text("SPARK", 45, 29)
    oled.show()
    sleep(2.5)
    oled.fill(0)
    oled.invert(0)
    oled.show()
    sleep(0.5)
    oled.text("Happy birthday!", 0, 8)
    oled.show()
    sleep(0.5)
    oled.text("zke!", 0, 23)
    oled.show()
    sleep(0.5)
    oled.text("2022.11.7", 0, 50)
    oled.show()
    sleep(0.5)
    sleep(8)
    oled.fill(0)
    oled.show()

def main():

    say_hello()

    spark_core = spark.SPARK()
    cont = 0
    while True:
        if cont == 0:
            x = random.randint(8, 120)
            y = random.randint(4, 60)
            spark_type = random.randint(1, 6)
            size = random.randint(5, 20)
            spark_core.spark_maker([x,y], spark_type, size)
            cont = 1
        else:
            cont = 0
        data = spark_core.screen_sequence.pop(0)
        spark_core.screen_sequence.append([])
        for point in data:
            oled.pixel(point[0], point[1], point[2])
            
        oled.show()




main()



