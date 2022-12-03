import ssd1306 as SSD1306_I2C
 
#lcd.imit_i2c(SCL引脚,SDA引脚,宽,长,i2c控制器编号官方图给出)
 
lcd.init_i2c(5,4, 128, 64, 0)
lcd.text('font8x8', 0, 0, 8)
lcd.text('font16x16', 0, 20, 16)
lcd.text('font24x24', 0, 40, 24)
lcd.show()
