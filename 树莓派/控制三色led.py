# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time

blue_p = 4
green_p = 3
red_p = 2


GPIO.setmode(GPIO.BCM)

 # 设置GPIO输入模式, 使用GPIO内置的下拉电阻, 即开关断开情况下输入为LOW
GPIO.setup(blue_p, GPIO.OUT)
 # 设置GPIO输入模式, 使用GPIO内置的下拉电阻, 即开关断开情况下输入为LOW
GPIO.setup(green_p, GPIO.OUT)
 # 设置GPIO输入模式, 使用GPIO内置的下拉电阻, 即开关断开情况下输入为LOW
GPIO.setup(red_p, GPIO.OUT)


js = 2
while True:

	js = js - 0.2

	GPIO.output(blue_p, GPIO.HIGH)
	time.sleep(js)
	GPIO.output(blue_p, GPIO.LOW)
	time.sleep(js)