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


strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()

def epilepsy(color):
    for i in range(300):
        strip.setPixelColor(i, color)
    time.sleep(0.01)
    strip.show()

while True:
    epilepsy(Color(255, 0, 0))
    epilepsy(Color(0, 0, 0))
    epilepsy(Color(0, 255, 0))
    epilepsy(Color(0, 0, 0))
    epilepsy(Color(0, 0, 255))
    epilepsy(Color(0, 0, 0))