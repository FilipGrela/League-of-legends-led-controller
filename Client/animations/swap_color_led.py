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
LED_BRIGHTNESS = 80     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

H_CHANGE_DIFFERENCE = 30 # Determines how much fluctuations in the color palette will be possible
S_RANGE = [95, 100]
V_RANGE = [80, 100]

MIN_H_DIFF = 20
MIN_S_DIFF = 1
MIN_V_DIFF = 8

UP = "\x1B[3A"
CLR = "\x1B[0K"

F_first_loop = True
last_random_h = None
last_random_s = None
last_random_v = None

random_h = 0
random_s = random.randint(S_RANGE[0], S_RANGE[1])
random_v = random.randint(V_RANGE[0], V_RANGE[1])

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
    for i in range(150):
        color = hsv2rgb(h, s, (v/150)*i)

        for j in range(i):
            strip.setPixelColor(149-j, Color(color[0], color[1], color[2]))
            strip.setPixelColor(150+j, Color(color[0], color[1], color[2]))

        sleep(0.02)
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


def get_random_h():
    next_random_h_range = []
    for i in range(H_CHANGE_DIFFERENCE):
        if (last_random_h - i - 1 > 0):
            next_random_h_range.append(last_random_h - i - 1)
        else:
            next_random_h_range.append(360 + last_random_h - i - 1)

        if (last_random_h + i + 1 < 360):
            next_random_h_range.append(last_random_h + i + 1)
        else:
            next_random_h_range.append(abs(360 - last_random_h + i + 1))

    return random.choice(next_random_h_range)

try:

    while True:

        if last_random_h == None: # Runs on first loop
            last_random_h = random_h

        else:
            while abs(last_random_h - random_h) < MIN_H_DIFF:
                random_h = get_random_h()

            while abs(last_random_s - random_s) < MIN_S_DIFF:
                random_s = random.randint(S_RANGE[0], S_RANGE[1])

            while abs(last_random_v - random_v) < MIN_V_DIFF:
                random_v = random.randint(V_RANGE[0], V_RANGE[1])

            print("HSV:")
            print(random_h, random_s, random_v)
            print("DIFF:")
            print(last_random_h - random_h, last_random_s - random_s, last_random_v - random_v)


#            print("{UP}HSV: {random_h}, {random_s}, {random_v}{CLR}\nDIF: {last_random_h - random_h}, {last_random_s - random_s}, {last_random_v - random_v}{CLR}\n")
        leds_set_color(random_h, random_s, random_v, True)

        last_random_h = random_h
        last_random_s = random_s
        last_random_v = random_v


except KeyboardInterrupt:
    leds_set_color(0, 0, 0, True)
