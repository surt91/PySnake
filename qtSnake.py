#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
import random
import sys

# TODO: orientiertes Dreieck als Kopf

class SnakeAnzeige(QtGui.QWidget):

    richtungen = {  "last"   : 0,
                    "oben"   : 1,
                    "unten"  : 2,
                    "links"  : 3,
                    "rechts" : 4}

    def __init__(self):
        super().__init__()


        max_x = 20
        max_y = 20

        # Initialisierungen
        self.__max_x = max_x
        self.__max_y = max_y

        self.__statusPause = True

        self.__spielfeld = [[0 for j in range(self.__max_y)] for i in range(self.__max_x)]

        start_x = self.__max_x // 2
        start_y = self.__max_y // 2

        self.__length = 3

        self.__spielfeld[start_x][start_y] = self.__length

        self.__radius = 10

        self.__dx = 15
        self.__dy = 15

        self._width = self.__max_x * self.__dx
        self._height = self.__max_y * self.__dy

        self.setMinimumSize(self._width, self._height)

        self.__orientierung = "oben"

        self.__x = start_x
        self.__y = start_y

        self.__futter = (random.randint(0,self.__max_x), random.randint(0,self.__max_y))

        self.__timer = QtCore.QTimer()
        self.__timer.timeout.connect(self.__steuern)
        self.__timer.start(300)

        self.show()

    def redraw(self):
        self.update()

    def paintEvent(self, event):
        self.__size = min(self.height(), self.width())
        self.__margin = self.__size / 100
        self.__bereich = QtCore.QRect(self.__margin, self.__margin, self.__size - 2*self.__margin, self.__size - 2*self.__margin)

        paint = QtGui.QPainter(self)

        paint.setFont(QtGui.QFont('Monospace', self.__size/7))
        paint.setRenderHint(QtGui.QPainter.Antialiasing)
        paint.eraseRect(self.geometry())
        self.malen(paint)

    def malen(self,paint):
        paint.setPen(QtGui.QColor(  0,   0,   0))
        paint.drawRect
        paint.setPen(QtGui.QColor(  0, 255,   0))
        paint.setBrush(QtGui.QBrush(QtCore.Qt.SolidPattern))
        paint.setBrush(QtGui.QColor(  0, 255,   0))
        x = self.__x
        y = self.__y
        dx = self.__dx
        dy = self.__dy
        radius = self.__radius

        for i in range(len(self.__spielfeld)):
            for j in range(len(self.__spielfeld[i])):
                if self.__spielfeld[i][j] > 0:
                    paint.drawChord(i*dx-radius, j*dy-radius, 2*radius, 2*radius, 0, 16 * 360)
        paint.drawChord(x*dx-radius*3/2, y*dy-radius*3/2, 3*radius, 3*radius, 0, 16 * 360)
        paint.setPen(QtGui.QColor(255,   0,   0))
        paint.setBrush(QtGui.QColor(255,   0,   0))
        paint.drawChord(self.__futter[0]*dx-radius/2, self.__futter[1]*dy-radius/2, radius, radius, 0, 16 * 360)
        self.update()

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
        self.redraw()

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

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.__ende()
        if event.key() == QtCore.Qt.Key_Escape:
            self.__ende()
        elif event.key() == QtCore.Qt.Key_W:
            self.__orientierung = self.richtungen["oben"]
            self.__statusPause = False
        elif event.key() == QtCore.Qt.Key_S:
            self.__orientierung = self.richtungen["unten"]
            self.__statusPause = False
        elif event.key() == QtCore.Qt.Key_A:
            self.__orientierung = self.richtungen["links"]
            self.__statusPause = False
        elif event.key() == QtCore.Qt.Key_D:
            self.__orientierung = self.richtungen["rechts"]
            self.__statusPause = False

def main():
    app = QtGui.QApplication(sys.argv)
    ex = SnakeAnzeige()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
