#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import pygame
import math
import sys

class Snake:

    richtungen = {  "last"   : 0,
                    "oben"   : 1,
                    "unten"  : 2,
                    "links"  : 3,
                    "rechts" : 4}

    def __init__(self, width, height):
        self.__fpsClock = pygame.time.Clock()

        self._width = width
        self._height = height
        pygame.init()
        self._screen = pygame.display.set_mode((self._width, self._height))
        self._screen.fill((0, 0, 0))
        pygame.display.update()

        self.__orientierung = "oben"

        self.__x = 400
        self.__y = 400

        self.__radius = 20

        self.__dx = 30
        self.__dy = 30

        pygame.time.set_timer(pygame.USEREVENT, 500)

    def malen(self):
        self._screen.fill((0,0,0))
        pygame.draw.circle(self._screen, (0,255,0), (self.__x, self.__y), self.__radius, 0)
        pygame.display.update()

    def __steuern(self):
        if self.__orientierung == self.richtungen["oben"]:
            self.__y -= self.__dy
        elif self.__orientierung == self.richtungen["unten"]:
            self.__y += self.__dy
        elif self.__orientierung == self.richtungen["links"]:
            self.__x -= self.__dx
        elif self.__orientierung == self.richtungen["rechts"]:
            self.__x += self.__dx
        self.malen()

    def __pause(self):
        pass

    def __ende(self):
        sys.exit()

    def event_loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__ende()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.__ende()
                    if event.key == pygame.K_p:
                        self.__pause()
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.__orientierung = self.richtungen["oben"]
                        self.__steuern()
                    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.__orientierung = self.richtungen["unten"]
                        self.__steuern()
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.__orientierung = self.richtungen["links"]
                        self.__steuern()
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.__orientierung = self.richtungen["rechts"]
                        self.__steuern()
                elif event.type == pygame.USEREVENT:
                    self.__steuern()
                    pygame.time.set_timer(pygame.USEREVENT, 500)
            self.__fpsClock.tick(30)

if __name__ == '__main__':
    a = Snake(800, 800)
    a.event_loop()
