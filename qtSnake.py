#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
import random
import sys

# TODO: orientiertes Dreieck als Kopf
# TODO: spielfeld als rect (schwarz)
# TODO: punktezähler
# TODO: Menüpunkt zur Anpassung der Spielfeldgröße
# TODO: mainwindows, und SnakeAnzeige als widget einbinden

class SnakeAnzeige(QtGui.QWidget):

    richtungen = {  "last"   : 0,
                    "oben"   : 1,
                    "unten"  : 2,
                    "links"  : 3,
                    "rechts" : 4}

    def __init__(self):
        super().__init__()

        maxFeld = (20, 20)

        self.__initUI()
        self.__initSnake(maxFeld)

    def __initUI(self):
        self.show()

    def __initSnake(self, maxFeld):
        # Initialisierungen
        self.__punkte = 0

        self.__maxF = maxFeld

        self.__statusPause = True

        self.__spielfeld = [[0 for j in range(self.__maxF[1])] for i in range(self.__maxF[0])]

        startF  = [i//2 for i in self.__maxF]

        self.__length = 3

        self.__spielfeld[startF[0]][startF[1]] = self.__length

        self.__radius = 10

        self.__dF = (15,15)

        self.__size = [i*j+self.__radius for i,j in zip(self.__maxF, self.__dF)]

        self.setMinimumSize(self.__size[0], self.__size[1])

        self.__orientierung = "oben"

        self.__pos = startF

        self.__futter = (random.randint(0,self.__maxF[0]), random.randint(0,self.__maxF[1]))

        self.__timer = QtCore.QTimer()
        self.__timer.timeout.connect(self.__steuern)
        self.__timer.start(300)

    def redraw(self):
        self.update()

    def paintEvent(self, event):
        #~ self.__size = min(self.height(), self.width())
        #~ self.__margin = self.__size / 100
        self.__bereich = QtCore.QRect(0, 0, self.__size[0], self.__size[1])

        paint = QtGui.QPainter(self)

        paint.setBrush(QtGui.QBrush(QtCore.Qt.SolidPattern))
        #~ paint.setFont(QtGui.QFont('Monospace', self.__size/7))
        paint.setRenderHint(QtGui.QPainter.Antialiasing)
        paint.eraseRect(self.__bereich)
        self.malen(paint)

    def malen(self,paint):
        paint.setPen(QtGui.QColor(  0,   0,   0))
        paint.setBrush(QtGui.QColor(  0,   0,   0))
        paint.drawRect(self.__bereich)
        paint.setPen(QtGui.QColor(  0, 255,   0))
        paint.setBrush(QtGui.QColor(  0, 255,   0))
        x = self.__pos[0]
        y = self.__pos[1]
        dx = self.__dF[0]
        dy = self.__dF[1]
        radius = self.__radius

        for i in range(len(self.__spielfeld)):
            for j in range(len(self.__spielfeld[i])):
                if self.__spielfeld[i][j] > 0:
                    paint.drawChord((i+1)*dx-radius, (j+1)*dy-radius, 2*radius, 2*radius, 0, 16 * 360)
        paint.drawChord((x+1)*dx-radius*3/2, (y+1)*dy-radius*3/2, 3*radius, 3*radius, 0, 16 * 360)
        paint.setPen(QtGui.QColor(255,   0,   0))
        paint.setBrush(QtGui.QColor(255,   0,   0))
        paint.drawChord((self.__futter[0]+1)*dx-radius/2, (self.__futter[1]+1)*dy-radius/2, radius, radius, 0, 16 * 360)
        self.update()

    def __steuern(self):
        for i in range(len(self.__spielfeld)):
            for j in range(len(self.__spielfeld[i])):
                if self.__spielfeld[i][j] > 0:
                    self.__spielfeld[i][j] -= 1
        if self.__orientierung == self.richtungen["oben"]:
            self.__pos[1] -= 1
        elif self.__orientierung == self.richtungen["unten"]:
            self.__pos[1] += 1
        elif self.__orientierung == self.richtungen["links"]:
            self.__pos[0] -= 1
        elif self.__orientierung == self.richtungen["rechts"]:
            self.__pos[0] += 1

        self.__testWand()
        self.__testSchwanz()
        self.__testFutter()

        self.__spielfeld[self.__pos[0]][self.__pos[1]] = self.__length
        self.redraw()

    def __testWand(self):
        for i in (0,1):
            if self.__pos[i] >= self.__maxF[i]:
                self.__pos[i] = 0
            if self.__pos[i] <= 0-1:
                self.__pos[i] = self.__maxF[i]-1

    def __testSchwanz(self):
        if self.__spielfeld[self.__pos[0]][self.__pos[1]] != self.__length -1  and self.__spielfeld[self.__pos[0]][self.__pos[1]] != 0:
            print(self.__pos[0], self.__pos[1], ":", self.__spielfeld[self.__pos[0]][self.__pos[1]])
            print("Verloren")
            #~ self.__verloren()

    def __testFutter(self):
        if self.__pos[0] == self.__futter[0] and self.__pos[1] == self.__futter[1]:
            self.__futter = (random.randint(0,self.__maxF[0]-1), random.randint(0,self.__maxF[1]-1))
            self.__length += 1
            for i in range(len(self.__spielfeld)):
                for j in range(len(self.__spielfeld[i])):
                    if self.__spielfeld[i][j] > 0:
                        self.__spielfeld[i][j] += 1

    def __pause(self):
        if self.__statusPause:
            self.__statusPause = False
        else:
            self.__statusPause = True

    def __verloren(self):
        sys.exit()

    def __ende(self):
        sys.exit()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.__ende()
        if event.key() == QtCore.Qt.Key_Escape:
            self.__ende()
        elif event.key() == QtCore.Qt.Key_W:
            if self.__orientierung != self.richtungen["unten"]:
                self.__orientierung = self.richtungen["oben"]
                self.__statusPause = False
        elif event.key() == QtCore.Qt.Key_S:
            if self.__orientierung != self.richtungen["oben"]:
                self.__orientierung = self.richtungen["unten"]
                self.__statusPause = False
        elif event.key() == QtCore.Qt.Key_A:
            if self.__orientierung != self.richtungen["rechts"]:
                self.__orientierung = self.richtungen["links"]
                self.__statusPause = False
        elif event.key() == QtCore.Qt.Key_D:
            if self.__orientierung != self.richtungen["links"]:
                self.__orientierung = self.richtungen["rechts"]
                self.__statusPause = False

def main():
    app = QtGui.QApplication(sys.argv)
    ex = SnakeAnzeige()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
