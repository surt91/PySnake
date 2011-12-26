#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
import random
import os
from snakeAnzeige import *
from highscore import *

class Snake(QtGui.QWidget):
    richtungen = {  "last"   : 0,
                    "oben"   : 1,
                    "unten"  : 2,
                    "links"  : 3,
                    "rechts" : 4}
    farben = { "bg"       : QtGui.QColor(  0,   0,   0),
               "futter"   : QtGui.QColor(255,   0,   0),
               "schlange" : QtGui.QColor(  0, 255,   0) }

    def __init__(self):
        super().__init__()
        self.__punkte = 0
        self.__maxF = (20, 20)

        self.initUI()

        self.__initSnake()

    def initUI(self):
        self.punktAnzeige = QtGui.QLabel()
        self.__setPunkte(0)

        self.pauseAnzeige = QtGui.QLabel()
        self.setPause(True)

        self.__initAnzeige()

        statusAnzeige = QtGui.QVBoxLayout()
        statusAnzeige.addWidget(self.pauseAnzeige)
        statusAnzeige.addWidget(self.punktAnzeige)
        statusAnzeige.addStretch()

        display = QtGui.QHBoxLayout()
        display.addWidget(self.anzeige)
        display.addLayout(statusAnzeige)

        self.setLayout(display)

        self.show()

    def __initAnzeige(self):
        self.anzeige = SnakeAnzeige(self.__maxF, self.richtungen, self.farben)

    def redraw(self):
        self.anzeige.setColor(self.farben)
        self.anzeige.setPos(self.__pos)
        self.anzeige.setFutter(self.__futter)
        self.anzeige.setOrientierung(self.__orientierung)
        self.anzeige.setSpielfeld(self.__spielfeld)
        self.anzeige.update()

    def __initSnake(self):
        # Initialisierungen
        self.__level = 3

        self.setColor(self.farben)

        self.neustart()

    def neustart(self):
        self.__pAutopilot = False
        self.__bVerloren = False
        self.__setPunkte(0)

        self.setPause(True)
        self.__block = False

        self.anzeige.setMaxF(self.__maxF)

        self.__spielfeld = [[0 for j in range(self.__maxF[1])] for i in range(self.__maxF[0])]

        startF  = [i//2 for i in self.__maxF]

        self.__length = 3

        self.__spielfeld[startF[0]][startF[1]] = self.__length

        self.__orientierung = self.richtungen["oben"]

        self.__pos = startF

        self.__genFutter()

        self.__timer = QtCore.QTimer()
        self.__timer.timeout.connect(self.__steuern)
        self.__timer.start(1000/self.__level/2)

        self.anzeige.neustart()
        self.redraw()

    def __steuern(self):
        if not self.__statusPause:
            for i in range(len(self.__spielfeld)):
                for j in range(len(self.__spielfeld[i])):
                    if self.__spielfeld[i][j] > 0:
                        self.__spielfeld[i][j] -= 1

            if self.__pAutopilot:
                self.autopilot()

            if self.__orientierung == self.richtungen["oben"]:
                self.__pos[1] -= 1
            elif self.__orientierung == self.richtungen["unten"]:
                self.__pos[1] += 1
            elif self.__orientierung == self.richtungen["links"]:
                self.__pos[0] -= 1
            elif self.__orientierung == self.richtungen["rechts"]:
                self.__pos[0] += 1
            self.__block = False

            self.__testFeldVoll()
            self.__testWand()
            self.__testSchwanz()
            self.__testFutter()

            self.__spielfeld[self.__pos[0]][self.__pos[1]] = self.__length
            self.redraw()

    def __testFeldVoll(self):
        n=0
        for i in range(len(self.__spielfeld)):
                for j in range(len(self.__spielfeld[i])):
                    if self.__spielfeld[i][j] == 0:
                        n += 1
        if n <= 2:
            self.__verloren()

    def __testWand(self):
        for i in (0,1):
            if self.__pos[i] >= self.__maxF[i]:
                self.__pos[i] = 0
            if self.__pos[i] <= 0-1:
                self.__pos[i] = self.__maxF[i]-1

    def __testSchwanz(self):
        if self.__spielfeld[self.__pos[0]][self.__pos[1]] != self.__length -1  and self.__spielfeld[self.__pos[0]][self.__pos[1]] != 0:
            self.__verloren()

    def __testFutter(self):
        if self.__pos[0] == self.__futter[0] and self.__pos[1] == self.__futter[1]:
            self.__genFutter()
            self.__length += 1
            self.__setPunkte(self.__level, add=True)

            for i in range(len(self.__spielfeld)):
                for j in range(len(self.__spielfeld[i])):
                    if self.__spielfeld[i][j] > 0:
                        self.__spielfeld[i][j] += 1

    def __genFutter(self):
        while True:
            i = random.randint(0,self.__maxF[0]-1)
            j = random.randint(0,self.__maxF[1]-1)
            if self.__spielfeld[i][j] == 0 and self.__pos != [i,j]:
                break
        self.__futter = (i,j)

    def __setPunkte(self, p, add = False):
        if add:
            self.__punkte += p
        else:
            self.__punkte = p
        self.punktAnzeige.setText("Punkte: " + "{:04d}".format(self.__punkte))

    def togglePause(self):
        if self.__statusPause:
            self.setPause(False)
        else:
            self.setPause(True)

    def setPause(self, p):
        if p:
            self.__statusPause = True
            self.pauseAnzeige.setText("Pause!")
        else:
            if not self.__bVerloren:
                self.__statusPause = False
                self.pauseAnzeige.setText("")

    def __verloren(self):
        self.__bVerloren = True
        self.setPause(True)
        try:
            name = os.environ['USER']
        except:
            newString = "Anon"
        if self.__pAutopilot:
            name = "bot"
        self.pauseAnzeige.setText("Verloren!")
        if CheckHighscore.getPunkte() < self.__punkte\
                                    or CheckHighscore.getLength() < 10:
            hs = SetHighscore(self.__punkte, self.__level, self.__maxF, name)
            hs2 = ShowHighscore()
            hs2.exec_()

    def __ende(self):
        sys.exit()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.__ende()
        if event.key() == QtCore.Qt.Key_P:
            self.togglePause()
        if not self.__block:
            if event.key() == QtCore.Qt.Key_W:
                if self.__orientierung != self.richtungen["unten"]:
                    self.__orientierung = self.richtungen["oben"]
                    self.__block = True
                    self.setPause(False)
            elif event.key() == QtCore.Qt.Key_S:
                if self.__orientierung != self.richtungen["oben"]:
                    self.__orientierung = self.richtungen["unten"]
                    self.__block = True
                    self.setPause(False)
            elif event.key() == QtCore.Qt.Key_A:
                if self.__orientierung != self.richtungen["rechts"]:
                    self.__orientierung = self.richtungen["links"]
                    self.__block = True
                    self.setPause(False)
            elif event.key() == QtCore.Qt.Key_D:
                if self.__orientierung != self.richtungen["links"]:
                    self.__orientierung = self.richtungen["rechts"]
                    self.__block = True
                    self.setPause(False)

    def setLevel(self, i):
        self.__level = i

    def getLevel(self):
        return self.__level

    def setSize(self, i):
        self.__maxF = i

    def getSize(self):
        return self.__maxF

    def setColor(self, colors):
        self.farben = colors
        self.anzeige.setColor(colors)

    def getColor(self):
        return self.farben

    def toggleAutopilot(self):
        if self.__pAutopilot:
            self.__pAutopilot = False
        else:
            self.__pAutopilot = True

    def autopilot(self):
        wunsch = [0,0,0,0]

        x = self.__futter[0] - self.__pos[0]
        y = self.__futter[1] - self.__pos[1]

        l = abs(x) if x < 0 else abs(self.__maxF[0] - abs(x))
        r = abs(x) if x > 0 else abs(self.__maxF[0] - abs(x))

        o = abs(y) if y < 0 else abs(self.__maxF[1] - abs(y))
        u = abs(y) if y > 0 else abs(self.__maxF[1] - abs(y))

        gewichte = [("links",l),("rechts",r),("oben",o),("unten",u)]
        g = [gewichte[i][1] for i in range(len(gewichte))]

        for j,k in zip(range(3, -1, -1), range(4)):
            for i in range(j+1):
                if gewichte[i][1] == min(g):
                    wunsch[k] = self.richtungen[gewichte[i][0]]
                    del gewichte[i]
                    del g[i]
                    break

        for n in range(3, -1, -1):
            for i in wunsch:
                tmp = True
                for j in range(n, 0, -1):
                    if not self.__testWeg(i,j):
                        tmp = False
                if tmp:
                    self.__orientierung = i
                    break
            if tmp:
                break

    def __testWeg(self, richtung, n):
        if richtung == self.richtungen["unten"]:
            if self.__orientierung != self.richtungen["oben"]:
                if self.__spielfeld[self.__pos[0]][(self.__pos[1]+n) % self.__maxF[1]] == 0:
                    return True
        elif richtung == self.richtungen["oben"]:
            if self.__orientierung != self.richtungen["unten"]:
                if self.__spielfeld[self.__pos[0]][(self.__pos[1]-n) % self.__maxF[1]] == 0:
                    return True
        elif richtung == self.richtungen["rechts"]:
            if self.__orientierung != self.richtungen["links"]:
                if self.__spielfeld[(self.__pos[0]+n) % self.__maxF[0]][self.__pos[1]] == 0:
                    return True
        elif richtung == self.richtungen["links"]:
            if self.__orientierung != self.richtungen["rechts"]:
                if self.__spielfeld[(self.__pos[0]-n) % self.__maxF[0]][self.__pos[1]] == 0:
                    return True
        return False
