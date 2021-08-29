from rpi_ws281x import *
import argparse
import colorsys
from time import sleep
import random

LED_COUNT      = 300      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 30     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53


def hsv2rgb(h,s,v):
    if h != 0:
        h = h/360
    if s != 0:
        s = s/100
    if v != 0:
        v = v/100
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))

def leds_set_color(h, s, v):
    for i in range(150): 
        color = hsv2rgb(h, s, (v/150)*i)
        for j in range(i):
            strip.setPixelColor(149-j, Color(color[0], color[1], color[2]))
            strip.setPixelColor(150+j, Color(color[0], color[1], color[2]))

        if i % 0.5 == 0 or i > 145:
            strip.show()
    strip.show()

parser = argparse.ArgumentParser(description='Enter hsv values.')
parser.add_argument('-o', '--hue',  type=int, help='Hue value')
parser.add_argument('-n', '--saturation',  type=int, help='Saturation value.')
parser.add_argument('-w', '--value',  type=int, help='Color value.')
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

    if args.hue != None and args.saturation!= None and args.value!= None:
        if args.hue > 360 or args.saturation > 100 or args.value > 100 or args.brightness > 255:
            print("--------------------Incorrect value--------------------\n   -o max value is 360 where 0 red, 120 green, 240 blue\n   -n nax value is 100\n   -w max value is 100\n   -j max value is 255")
        leds_set_color(args.hue, args.saturation, args.value
    else:
        leds_set_color(320, 95, 100)
except KeyboardInterrupt:
    leds_set_color(0, 0, 0)
