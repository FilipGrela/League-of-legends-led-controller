from time import sleep
from rpi_ws281x import *
import argparse

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

def meteorRain(red, green, blue, meteorSize, meteorTrailDecay, meteorRandomDecay, SpeedDelay):
    for i in range(LED_COUNT*2):

        # for j in range(LED_COUNT):
        #     if meteorRandomDecay == False or random.randint(10) > 5:
        #         fadeToBlack(j, meteorTrailDecay)
        
        for j in range(meteorSize):
            if i-j < LED_COUNT and i-j>=0:
                print(i-j)
                strip.setPixelColor(i-j, Color(red, green, blue))

    strip.show()
    sleep(SpeedDelay)

# def fadeToBlack(ledNo, fadeValue):


while True:
    meteorRain(255, 20, 25, 10, 64, True, 30)