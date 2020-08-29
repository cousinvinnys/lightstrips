#!/usr/bin/env python3

import board
import neopixel
from neopixel import NeoPixel
from time import sleep

if __name__ == '__main__':
    pixels = NeoPixel(board.D18, 150)
    colors = [(255,0,0),(255,255,0),(0,255,0),(0,255,255),(0,0,255),(255,0,255)]
    while True:
        for i in pixels:
            pixels.fill(i)
            sleep(1)