#!/usr/bin/env python3
import pygame
from pygame.locals import *


class VirtualPixels:
    def __init__(self, board_stuff, length, auto_write=False):
        pygame.init()
        self.length = length
        self.screen = pygame.display.set_mode((length * 5 + 1, 7))
        pygame.display.set_caption("Virtual Light Strips")
        self._pixels = [(0, 0, 0)] * length
        self.clock = pygame.time.Clock()

    def show(self):
        self.clock.tick(30)
        pygame.event.pump()
        self.screen.fill((000, 000, 000))

        keystate = pygame.key.get_pressed()

        for i in range(self.length):
            pygame.draw.circle(self.screen, self._pixels[i], (i * 5 + 3, 3), 2, 2)

        pygame.display.update()

    def __getitem__(self, index):
        return self._pixels[index]

    def __setitem__(self, index, value):
        self._pixels[index] = value

    def __len__(self):
        return len(self._pixels)


class VirtualBoard:
    D18 = None
