import socket
import time
import json
from rpi_ws281x import *
import argparse
from random import randrange
import colorsys

TICK_RATE = 0.3
SERVER = "192.168.8.136"
PORT = 6060
ADDR = (SERVER, PORT)
HEADER = 64
FORMAT = 'utf-8'
EXIT_MSG = "Az!DaKYJ,2LvN=]s{R@];4))#Aj-hub<tuP4D+^S8RN,Yb+r_+"

LED_COUNT      = 300      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 60     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

COLOR_WHILE_ALIVE = Color(50, 218, 54)

strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send_messaeg(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

def recive_message():
    msg_lenght = client.recv(HEADER).decode(FORMAT)
    if msg_lenght:
        msg_lenght = int(msg_lenght)
        msg = str(client.recv(msg_lenght).decode(FORMAT))
        print("[MESSAGE RECIVED]:" + msg)
        on_message(msg)

def on_message(msg):
    if msg == "new assist":
        led_event_animation(Color(235, 168, 0))
    elif msg == "new creep score":
        led_event_animation(Color(170, 0, 155))
    elif msg == "new death":
        pass
        # led_event_animation(Color(158, 0, 0))
    elif msg == "new kill":
        led_event_animation(Color(0, 255, 0))
    elif msg == "new wardScore":
        led_event_animation(Color(0, 193, 255))
    elif msg == "new purchase":
        led_event_animation(Color(255, 40, 0))
    elif msg == "level up":
        led_event_animation(Color(187, 128, 255))
    elif msg == "ping_message":
        pass
    else:
        respawn_time = float(msg.split(".")[0])
        print(respawn_time)
        leds_set_color(Color(158, 0, 0), respawn_time + 0.3)
        leds_set_color(COLOR_WHILE_ALIVE)

# def led_while_dead(respawn_time):
#     leds_per_100ms = round(150.0/respawn_time/10.0, 0)
#     print(leds_per_100ms)

#     strip.show()

def led_event_animation(color):
    animation_led_leinght = 100
    for i in range(150 + animation_led_leinght):
        if i > animation_led_leinght:
            if i < 150:
                strip.setPixelColor(150-i, color)
                strip.setPixelColor(149+i, color)

            strip.setPixelColor(150 + animation_led_leinght - i, COLOR_WHILE_ALIVE)
            strip.setPixelColor(150 - animation_led_leinght - 1 + i, COLOR_WHILE_ALIVE)
        else:
            strip.setPixelColor(149-i, color)
            strip.setPixelColor(150+i, color)


        if i % 3 == 0 or i > 145:
            strip.show()

def leds_set_color(color, sleep = 0):
    for i in range(150):
        strip.setPixelColor(149-i, color)
        strip.setPixelColor(150+i, color)
        if i % 8 == 0 or i > 145:
            strip.show()
    
    if sleep != 0:
            time.sleep(sleep)



def start():
    try:
        leds_set_color(COLOR_WHILE_ALIVE)

        while True:
            recive_message()
    except KeyboardInterrupt:
        send_messaeg(EXIT_MSG)
        leds_set_color(Color(0, 0, 0))
        pass

print("[STARTING] Client is starting....")
start()
