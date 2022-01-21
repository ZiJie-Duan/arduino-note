# Untitled - By: lucyc - 周二 1月 18 2022
import sensor, image, lcd, time
import KPU as kpu
import gc, sys
from Maix import freq


#freq.set(cpu = 590, pll1 = 590, kpu_div=1)
#freq.set(cpu = 500, pll1 = 500, kpu_div=1)
sensor.reset(freq=24000000)
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_auto_gain(1)
sensor.set_hmirror(0)
sensor.set_vflip(1)
sharp = (-1,-1,-1,-1,9,-1,-1,-1,-1)
edge = (-1,-1,-1,-1,8,-1,-1,-1,-1)

lcd.init()
clock = time.clock()

def draw_x(img,midpoint):
    mid_x = midpoint[0]
    mid_x_1 = mid_x - 15
    mid_x_2 = mid_x + 15
    mid_y = midpoint[1]
    mid_y_1 = mid_y - 15
    mid_y_2 = mid_y + 15
    img.draw_line(mid_x_1,mid_y,mid_x_2,mid_y,color=(255, 0, 0))
    img.draw_line(mid_x,mid_y_1,mid_x,mid_y_2,color=(255, 0, 0))
    return img

js = 0
while(True):
    clock.tick()
    js += 1
    img = sensor.snapshot()
    if js < 30:
        sensor.set_framesize(sensor.QVGA)
        img = img.resize(320,240)
        img = draw_x(img,[160,120])
        img.draw_string(10, 200, str(clock.fps()), scale=2)
        img.draw_string(10, 180, str("all")+str(js), scale=2)
        lcd.display(img)

    elif js < 60:
        sensor.set_framesize(sensor.VGA)
        imgn = img.copy(roi=(160, 120, 320, 240))
        imgn = draw_x(imgn,[160,120])
        imgn.draw_string(10, 200, str(clock.fps()), scale=2)
        imgn.draw_string(10, 180, str("mini")+str(js), scale=2)
        lcd.display(imgn)

    elif js < 90:
        sensor.set_framesize(sensor.VGA)
        img.conv3(edge)
        imgn = img.copy(roi=(240, 180, 160, 120))
        imgn = imgn.resize(320,240)
        imgn = draw_x(imgn,[160,120])
        imgn.draw_string(10, 200, str(clock.fps()), scale=2)
        imgn.draw_string(10, 180, str("mini")+str(js), scale=2)
        lcd.display(imgn)

    elif js > 90:
        js = 0

