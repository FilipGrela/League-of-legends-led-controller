import time
from rpi_ws281x import *
import argparse
import random


LED_COUNT      = 300      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 64     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

DEFAULT_COLOR = Color(255, 40, 0)


strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()

def led_event_animation(color):
    animation_led_leinght = 75
    for i in range(150 + animation_led_leinght):
        if i > animation_led_leinght:
            if i < 150:
                strip.setPixelColor(150-i, color)
                strip.setPixelColor(149+i, color)

            strip.setPixelColor(150 + animation_led_leinght - i, DEFAULT_COLOR)
            strip.setPixelColor(150 - animation_led_leinght - 1 + i, DEFAULT_COLOR)
        else:
            strip.setPixelColor(149-i, color)
            strip.setPixelColor(150+i, color)


        if i % 3 == 0 or i > 145:
            strip.show()

def leds_set_color(color):
    for i in range(150):
        strip.setPixelColor(149-i, color)
        strip.setPixelColor(150+i, color)
        if i % 8 == 0 or i > 145:
            strip.show()

while True:
    leds_set_color(DEFAULT_COLOR)
    time.sleep(0.2)
    led_event_animation(Color(255, 255, 255))
