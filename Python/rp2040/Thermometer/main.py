# I2C Scanner MicroPython
from machine import Pin, SoftI2C
import ssd1306
import utime
import aht10

# You can choose any other combination of I2C pins
oled_i2c = SoftI2C(scl=Pin(27), sda=Pin(26))

oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, oled_i2c)

aht_i2c = SoftI2C(sda=Pin(18), scl=Pin(19))
aht10 = aht10.AHT10(aht_i2c, mode=0, address=0x38)

dot = "."

while True:
    humi = aht10.humidity()
    temp = aht10.temperature()
    
    if len(dot) > 17:
        if "." not in dot:
            dot = "."
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