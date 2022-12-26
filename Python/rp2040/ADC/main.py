import ssd1327

# using Software I2C
from machine import SoftI2C, Pin
i2c = SoftI2C(sda=Pin(21), scl=Pin(22)) # TinyPICO
# i2c = SoftI2C(sda=Pin(0), scl=Pin(1)) # Raspberry Pi Pico
# i2c = SoftI2C(sda=Pin(4), scl=Pin(5)) # WeMos D1 Mini

# or using Hardware I2C
from machine import I2C, Pin
i2c = I2C(0) # TinyPICO sda=19, scl=18

display = ssd1327.SEEED_OLED_96X96(i2c)  # Grove OLED Display
# display = ssd1327.SSD1327_I2C(128, 128, i2c)  # WaveShare, Zio Qwiic

display.text('Hello World', 0, 0, 255)
display.show()

display.fill(0)
for y in range(0,12):
    display.text('Hello World', 0, y * 8, 15 - y)
display.show()