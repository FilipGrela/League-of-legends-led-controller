from rpi_ws281x import *
import argparse
import colorsys
from time import sleep
import random
import math
import sys 

LED_COUNT      = 300      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

UP = "\x1B[3A"
CLR = "\x1B[0K"

F_first_loop = True
last_random_h = None
last_random_s = None
last_random_v = None

F_show_broghtness_anim = None
last_set_v = None

def hsv2rgb(h,s,v):
    if h != 0:
        h = h/360
    if s != 0:
        s = s/100
    if v != 0:
        v = v/100
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))

def leds_set_color(h, s, v, fast=False):
    for i in range(int(LED_COUNT/2)): 
        color = hsv2rgb(h, s, (v/(LED_COUNT/2))*i)

        for j in range(int(LED_COUNT/2)):
            strip.setPixelColor(int((LED_COUNT/2-1)-j), Color(color[0], color[1], color[2]))
            strip.setPixelColor(int((LED_COUNT/2)+j), Color(color[0], color[1], color[2]))
        F_show_broghtness_anim = False
        sleep(0.01)
        strip.show()
    strip.show()

parser = argparse.ArgumentParser(description='Enter brightness values.')
parser.add_argument('-j', '--brightness', type=int, help='Led brightness.')
args = parser.parse_args()

if args.brightness != None:
    if args.brightness > 255:
        args.brightness = 255
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, args.brightness, LED_CHANNEL)
else:
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()

try:

    while True:
        random_h = random.randint(0, 360)
        random_s = random.randint(82, 100)
        random_v = random.randint(10, 60)
        if last_random_h == None:
            last_random_h = random_h
            last_random_s = random_s
            last_random_v = random_v

        while abs(last_random_h - random_h) > 50 or abs(last_random_h - random_h) < 30 and F_first_loop != True:
            random_h = random.randint(0, 360)
        
        while abs(last_random_s - random_s) < 6:
            random_s = random.randint(82, 100)

        while abs(last_random_v - random_v) < 20:
            random_v = random.randint(10, 60)

                
        print(f"{UP}HSV: {random_h}, {random_s}, {random_v}{CLR}\nDIF: {last_random_h - random_h}, {last_random_s - random_s}, {last_random_v - random_v}{CLR}\n")

        leds_set_color(random_h, random_s, random_v, True)

        last_random_h = random_h
        last_random_s = random_s
        last_random_v = random_v


except KeyboardInterrupt:
    leds_set_color(0, 0, 0, True)