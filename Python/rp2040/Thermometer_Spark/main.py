from machine import Pin, SoftI2C
import machine
import ssd1306
from time import sleep
import spark
import random
import utime
import aht10

machine.freq(120000000)

# You can choose any other combination of I2C pins
oled_i2c = SoftI2C(scl=Pin(27), sda=Pin(26))

oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, oled_i2c)

aht_i2c = SoftI2C(sda=Pin(18), scl=Pin(19))
aht10 = aht10.AHT10(aht_i2c, mode=0, address=0x38)

def thermoeter():
    dot = "."
    while True:
        humi = aht10.humidity()
        temp = aht10.temperature()
        
        if len(dot) > 15:
            if "." not in dot:
                dot = "."
                return humi
            else:
                dot = " "+ dot[:len(dot)-1]
        else:
            dot += "."

        oled.fill(0)
        oled.text("Thermometer", 0, 5)
        oled.text("Temp:", 0, 20)
        oled.text("Humi:", 0, 35)
        oled.text(str(temp), 40, 20)
        oled.text(str(humi), 40, 35)
        oled.text(dot, 0, 50)
        oled.show()
        utime.sleep(0.1)

def say_hello():
    oled.fill(0)
    oled.invert(1)
    oled.text("SPARK-Humi", 24, 29)
    oled.show()
    sleep(2)
    oled.fill(0)
    oled.invert(0)
    oled.show()
    sleep(0.8)
    oled.text("Try to blow", 0, 8)
    oled.text("towards me.", 0, 23)
    oled.text("2024/02/04", 0, 50)
    oled.show()
    sleep(0.5)
    sleep(2)
    oled.fill(0)
    oled.show()
    

def build_spark(spark_core):
    x = random.randint(8, 120)
    y = random.randint(4, 60)
    spark_type = random.randint(1, 6)
    size = random.randint(5, 20)
    spark_core.spark_maker([x,y], spark_type, size)

def pop_show_spark(spark_core, oled):
    data = spark_core.screen_sequence.pop(0)
    spark_core.screen_sequence.append([])
    for point in data:
        oled.pixel(point[0], point[1], point[2])
    oled.show()


def main():
    #humi_base = thermoeter()
    humi_base = 30
    say_hello()
    spark_core = spark.SPARK()
    
    while True:
        humi = aht10.humidity()
        diff = abs(int(humi - humi_base))
        
        bt = diff//6
        st = diff//2
        
        for i in range(st):
            if i < bt:
                build_spark(spark_core)
            else:
                utime.sleep(0.045)
                
            pop_show_spark(spark_core, oled)


main()



