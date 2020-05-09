from machine import Pin, I2C
import time
import json
i2c = I2C(scl=Pin(5), sda=Pin(4))

from ssd1306 import SSD1306_I2C
oled = SSD1306_I2C(128, 64, i2c)

oled.fill(1)
oled.show()
oled.fill(0)
oled.show()
a = 5/0
while True:
	with open("a.json") as zx:
		img = json.load(zx)
	img = img["a"]
	for zb in img:
		oled.pixel(zb[0], zb[1], 1)
	oled.show()
	time.sleep(0.5)
	oled.fill(0)
	img = []
	with open("b.json") as zx:
		img = json.load(zx)
	img = img["a"]
	for zb in img:
		oled.pixel(zb[0], zb[1], 1)
	oled.show()
	time.sleep(0.5)
	oled.fill(0)
	img = []
	with open("c.json") as zx:
		img = json.load(zx)
	img = img["a"]
	for zb in img:
		oled.pixel(zb[0], zb[1], 1)
	oled.show()
	time.sleep(0.5)
	oled.fill(0)
	img = []
	with open("d.json") as zx:
		img = json.load(zx)
	img = img["a"]
	for zb in img:
		oled.pixel(zb[0], zb[1], 1)
	oled.show()
	time.sleep(0.5)
	oled.fill(0)
	img = []
	with open("f.json") as zx:
		img = json.load(zx)
	img = img["a"]
	for zb in img:
		oled.pixel(zb[0], zb[1], 1)
	oled.show()
	time.sleep(0.5)
	oled.fill(0)
	img = []
