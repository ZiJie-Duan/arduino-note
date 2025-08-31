# Example using PIO to drive a set of WS2812 LEDs.

import array, time
from machine import Pin
import rp2
import math

# Configure the number of WS2812 LEDs.
NUM_LEDS = 48
PIN_NUM = 22
brightness = 0.2

@rp2.asm_pio(sideset_init=rp2.PIO.OUT_LOW, out_shiftdir=rp2.PIO.SHIFT_LEFT, autopull=True, pull_thresh=24)
def ws2812():
    T1 = 2
    T2 = 5
    T3 = 3
    wrap_target()
    label("bitloop")
    out(x, 1)               .side(0)    [T3 - 1]
    jmp(not_x, "do_zero")   .side(1)    [T1 - 1]
    jmp("bitloop")          .side(1)    [T2 - 1]
    label("do_zero")
    nop()                   .side(0)    [T2 - 1]
    wrap()


# Create the StateMachine with the ws2812 program, outputting on pin
sm = rp2.StateMachine(0, ws2812, freq=8_000_000, sideset_base=Pin(PIN_NUM))

# Start the StateMachine, it will wait for data on its FIFO.
sm.active(1)

# Display a pattern on the LEDs via an array of LED RGB values.
# ar = array.array("I", [0 for _ in range(NUM_LEDS)])

##########################################################################

def gaussian(x, mu=0, sigma=1):
    """
    MicroPython 版本的一维高斯函数实现。
    
    参数:
    - x: 自变量
    - mu: 均值（μ），默认 0
    - sigma: 标准差（σ），默认 1
    
    返回:
    - 高斯函数在 x 处的值
    """
    coeff = 1 / (sigma * math.sqrt(2 * math.pi))
    exponent = -((x - mu) ** 2) / (2 * sigma ** 2)
    return coeff * math.exp(exponent)

def gaussian_peak_1(x, mu=0, width=1):
    """
    生成一个峰值为 1 的高斯形状曲线，宽度可调。
    
    参数:
    - x: 输入值
    - mu: 峰值位置
    - width: 控制曲线宽度（越大越平缓）
    
    返回:
    - 曲线值，最大值为 1
    """
    return math.exp(-((x - mu) / width) ** 2)

class LEDD:
    
    def __init__(self, led_num = NUM_LEDS):
        self.led_num = led_num
        self.ar = array.array("I", [0 for _ in range(NUM_LEDS)])
    
    def pset(self, i, color):
        self.ar[i] = (color[1]<<16) + (color[0]<<8) + color[2]

    def show(self):
        dimmer_ar = array.array("I", [0 for _ in range(NUM_LEDS)])
        for i,c in enumerate(self.ar):
            r = int(((c >> 8) & 0xFF) * brightness)
            g = int(((c >> 16) & 0xFF) * brightness)
            b = int((c & 0xFF) * brightness)
            dimmer_ar[i] = (g<<16) + (r<<8) + b
        sm.put(dimmer_ar, 8)
    
    def fill(self, color):
        for i in range(self.led_num):
            self.pset(i, color)
    
    def set_ar(self, ar):
        self.ar = ar


            
class Sun:
    
    def __init__(self, led):
        self.sigma = 2
        self.mu = 0
        self.speed = 0
        self.led = led
        self.color_set = (0,0,0)
        
    def _to_color(self, i):
        r = self.color_set[0] * i
        g = self.color_set[1] * i
        b = self.color_set[2] * i
        return int(r), int(g), int(b)
        #return (max(int(r),25), max(int(g),22), max(int(b),15))
    
    def _set_color(self,r,g,b):
        self.color_set=(r,g,b)
    
    def _get_sample(self):
        self.led.fill((0,0,0))
        for i in range(48):
            self.led.pset(i, self._to_color(gaussian_peak_1(i, self.mu - 4, self.sigma)))
    
    def _speed_change(self):
        #self. mu max 58
        abs_mu = max(0, self.mu)
        #print(abs_mu, 0.06 + 0.0035 * (26 - abs(22-abs_mu)))
        self.speed = 0.05 + 0.0015 * (26 - abs(22-abs_mu))
        
    def _day_sigma_change(self):
        #self. mu max 58
        abs_mu = max(0, self.mu)
        #print(abs_mu, 0.06 + 0.0035 * (26 - abs(22-abs_mu)))
        self.sigma = 2 + 0.15 * (26 - abs(25-abs_mu))
        #print(self.sigma)
    
    def _day_color_change(self):
        #self. mu max 58
        abs_mu = max(0, self.mu)
        #print(abs_mu, 0.06 + 0.0035 * (26 - abs(22-abs_mu)))
        r = self.color_set[0]
        g = self.color_set[1] - 6.5 * abs(25-abs_mu) 
        b = max(0,self.color_set[2] - 8 * abs(25-abs_mu))
        self._set_color(r,g,b)
        
    def _day_time(self):
        self.sigma = 2
        self.mu = 0
        self._set_color(255, 220, 150)
        for _ in range(800):
            self._set_color(255, 220, 150)
            self._day_color_change()
            print(self.mu)
            #print(self.color_set)
            self._day_sigma_change()
            self._speed_change()
            self.mu += self.speed
            self._get_sample()
            led.show()
            
    
    def _night_time(self):
        self.sigma = 2
        self.mu = 0.2
        self._set_color(60, 70, 150)
        self.speed = 0.1
        for _ in range(550):
            self.mu += self.speed - 0.003 * max(0, (10 - self.mu))
            self._get_sample()
            led.show()
            
                
    def run(self):
        while True:
            self._day_time()
            self._night_time()
            

print("st")
led = LEDD()
s = Sun(led)
time.sleep(5)
s.run()
print("end")

#[50, 10 , 0] 日出
#[100, 50, 10] 上午
#[250, 150, 130] 正午
#