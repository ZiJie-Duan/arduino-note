# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time
import smbus
import logx
import logging
BUS = smbus.SMBus(1)
LCD_ADDR = 0x27
BLEN = 1 #turn on/off background light

blue_p = 21
green_p = 20
red_p = 16

GPIO.setmode(GPIO.BCM)
 # 设置GPIO输入模式, 使用GPIO内置的下拉电阻, 即开关断开情况下输入为LOW
GPIO.setup(blue_p, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
 # 设置GPIO输入模式, 使用GPIO内置的下拉电阻, 即开关断开情况下输入为LOW
GPIO.setup(green_p, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
 # 设置GPIO输入模式, 使用GPIO内置的下拉电阻, 即开关断开情况下输入为LOW
GPIO.setup(red_p, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

# 检测LOW -> HIGH的变化
GPIO.add_event_detect(green_p, GPIO.RISING, bouncetime = 200)
# 检测LOW -> HIGH的变化
GPIO.add_event_detect(red_p, GPIO.RISING, bouncetime = 200)
# 检测LOW -> HIGH的变化
GPIO.add_event_detect(blue_p, GPIO.RISING, bouncetime = 200)



def turn_light(key):
  global BLEN
  BLEN = key
  if key ==1 :
    BUS.write_byte(LCD_ADDR ,0x08)
    logging.info('LCD executed turn on BLight')
  else:
    BUS.write_byte(LCD_ADDR ,0x00)
    logging.info('LCD executed turn off BLight')

def write_word(addr, data):
  global BLEN
  temp = data
  if BLEN == 1:
    temp |= 0x08
  else:
    temp &= 0xF7
  BUS.write_byte(addr ,temp)

def send_command(comm):
  # Send bit7-4 firstly
  buf = comm & 0xF0
  buf |= 0x04               # RS = 0, RW = 0, EN = 1
  write_word(LCD_ADDR ,buf)
  time.sleep(0.002)
  buf &= 0xFB               # Make EN = 0
  write_word(LCD_ADDR ,buf)
  
  # Send bit3-0 secondly
  buf = (comm & 0x0F) << 4
  buf |= 0x04               # RS = 0, RW = 0, EN = 1
  write_word(LCD_ADDR ,buf)
  time.sleep(0.002)
  buf &= 0xFB               # Make EN = 0
  write_word(LCD_ADDR ,buf)

def send_data(data):
  # Send bit7-4 firstly
  buf = data & 0xF0
  buf |= 0x05               # RS = 1, RW = 0, EN = 1
  write_word(LCD_ADDR ,buf)
  time.sleep(0.002)
  buf &= 0xFB               # Make EN = 0
  write_word(LCD_ADDR ,buf)
  
  # Send bit3-0 secondly
  buf = (data & 0x0F) << 4
  buf |= 0x05               # RS = 1, RW = 0, EN = 1
  write_word(LCD_ADDR ,buf)
  time.sleep(0.002)
  buf &= 0xFB               # Make EN = 0
  write_word(LCD_ADDR ,buf)

def init_lcd():
  try:
    send_command(0x33) # Must initialize to 8-line mode at first
    time.sleep(0.005)
    send_command(0x32) # Then initialize to 4-line mode
    time.sleep(0.005)
    send_command(0x28) # 2 Lines & 5*7 dots
    time.sleep(0.005)
    send_command(0x0C) # Enable display without cursor
    time.sleep(0.005)
    send_command(0x01) # Clear Screen
    logging.info('LCD init over')
    BUS.write_byte(LCD_ADDR ,0x08)
    logging.info('LCD turning on BLight')
  except:
    return False
  else:
    return True

def clear_lcd():
  send_command(0x01) # Clear Screen

def print_lcd(x, y, str):
  if x < 0:
    x = 0
  if x > 15:
    x = 15
  if y <0:
    y = 0
  if y > 1:
    y = 1

  # Move cursor
  addr = 0x80 + 0x40 * y + x
  send_command(addr)
  
  for chr in str:
    send_data(ord(chr))



def get_string_print_data(one,two):
	if one == 0:
		clear_lcd()
		print_lcd(0, 0, "ABCDEFGHIJKLMN")
		print_lcd(two, 1, "A")

	else:
		clear_lcd()
		print_lcd(0, 0, "OPQRSTUVWXYZkq")
		print_lcd(two, 1, "A")



def get_string():
	strlist = []
	zdlist = [["A","B","C","D","E","F","G","H","I","J","K","L","M","N"]\
	,["O","P","Q","R","S","T","U","V","W","X","Y","Z"," ","q"]]
	ys = 0
	zz = 0
	get_string_print_data(ys,zz)

	while True:

		if GPIO.event_detected(blue_p):
			if zz == 13:
				zz = 0
			else:
				zz = zz + 1

			get_string_print_data(ys,zz)


		elif GPIO.event_detected(green_p):

			zz = 0
			if ys == 1:
				ys = 0
			else:
				ys = ys + 1

			get_string_print_data(ys,zz)


		elif GPIO.event_detected(red_p):

			if zz == 13 and ys == 1:
				break

			strlist.append(zdlist[ys][zz])
			zz = 0
			ys = 0
			get_string_print_data(ys,zz)


	restr = ""
	for x in strlist:
		restr = restr + x


	print(restr)

	return restr


def s_server():
	



def main():
	init_lcd()
	clear_lcd()
	print_lcd(0, 0, "Talk to SXY")
	print_lcd(0, 1, "system V1.0")

	time.sleep(3)
	clear_lcd()

main()


# 清理占用的GPIO资源
GPIO.cleanup()

