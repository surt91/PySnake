#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pygame
import math
import sys
import random

class Snake:

    richtungen = {  "last"   : 0,
                    "oben"   : 1,
                    "unten"  : 2,
                    "links"  : 3,
                    "rechts" : 4}

    def __init__(self, max_x, max_y):
        self.__fpsClock = pygame.time.Clock()
        self.__statusPause = True

        self.__spielfeld = [[0 for j in range(max_y)] for i in range(max_x)]

        self.__max_x = max_x
        self.__max_y = max_y

        start_x = max_x // 2
        start_y = max_y // 2

        self.__length = 3

        self.__spielfeld[start_x][start_y] = self.__length

        self.__radius = 10

        self.__dx = 15
        self.__dy = 15

        self._width = max_x * self.__dx
        self._height = max_y * self.__dy

        pygame.init()
        self._screen = pygame.display.set_mode((self._width, self._height))
        self._screen.fill((0, 0, 0))
        pygame.display.update()

        self.__orientierung = "oben"

        self.__x = start_x
        self.__y = start_y

        self.__futter = (random.randint(0,self.__max_x), random.randint(0,self.__max_y))

        self.malen()

        pygame.time.set_timer(pygame.USEREVENT, 500)

    def malen(self):
        self._screen.fill((0,0,0))
        for i in range(len(self.__spielfeld)):
            for j in range(len(self.__spielfeld[i])):
                if self.__spielfeld[i][j] > 0:
                    pygame.draw.circle(self._screen, (0,255,0), (i*self.__dx,j*self.__dy), self.__radius, 0)
        pygame.draw.circle(self._screen, (0,255,0), (self.__x*self.__dx,self.__y*self.__dy), int(self.__radius*1.5), 0)
        pygame.draw.circle(self._screen, (255,0,0), (self.__futter[0]*self.__dx,self.__futter[1]*self.__dy), self.__radius, 0)
        pygame.display.update()

    def __steuern(self):
        for i in range(len(self.__spielfeld)):
            for j in range(len(self.__spielfeld[i])):
                self.__spielfeld[i][j] -= 1
        if self.__orientierung == self.richtungen["oben"]:
            self.__y -= 1
        elif self.__orientierung == self.richtungen["unten"]:
            self.__y += 1
        elif self.__orientierung == self.richtungen["links"]:
            self.__x -= 1
        elif self.__orientierung == self.richtungen["rechts"]:
            self.__x += 1

        self.__testWand()
        self.__testFutter()

        self.__spielfeld[self.__x][self.__y] = self.__length

    def __testWand(self):
        if self.__x >= self.__max_x:
            self.__x = 0
        if self.__x <= 0-1:
            self.__x = self.__max_x-1
        if self.__y >= self.__max_y:
            self.__y = 0
        if self.__y <= 0-1:
            self.__y = self.__max_y-1

    def __testFutter(self):
        if self.__x == self.__futter[0] and self.__y == self.__futter[1]:
            self.__futter = (random.randint(0,self.__max_x-1), random.randint(0,self.__max_y-1))
            self.__length += 1
            for i in range(len(self.__spielfeld)):
                for j in range(len(self.__spielfeld[i])):
                    self.__spielfeld[i][j] += 1

    def __pause(self):
        if self.__statusPause:
            self.__statusPause = False
        else:
            self.__statusPause = True

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
                        self.__togglePause()
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.__orientierung = self.richtungen["oben"]
                        self.__statusPause = False
                    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.__orientierung = self.richtungen["unten"]
                        self.__statusPause = False
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.__orientierung = self.richtungen["links"]
                        self.__statusPause = False
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.__orientierung = self.richtungen["rechts"]
                        self.__statusPause = False
                elif event.type == pygame.USEREVENT:
                    if not self.__statusPause:
                        self.__steuern()
                        self.malen()
                        pygame.time.set_timer(pygame.USEREVENT, 500)
            self.__fpsClock.tick(30)

if __name__ == '__main__':
    a = Snake(20, 20)
    a.event_loop()
