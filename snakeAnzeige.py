#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore

class SnakeAnzeige(QtGui.QWidget):
    def __init__(self, maxF, richtungen, farben):
        super().__init__()
        self.__initUI()

        self.__maxF = maxF
        self.richtungen = richtungen
        self.farben = farben

        self.__radius = 10
        self.__dF = (15,15)
        self.neustart()

    def neustart(self):
        self.__size = [i*j+self.__radius for i,j in zip(self.__maxF, self.__dF)]
        self.setMinimumSize(self.__size[0], self.__size[1])

    def __initUI(self):
        self.show()

    def setPos(self, pos):
        self.__pos = pos
    def setOrientierung(self, o):
        self.__orientierung = o
    def setMaxF(self, f):
        self.__maxF = f
    def setSpielfeld(self, f):
        self.__spielfeld = f
    def setFutter(self, pos):
        self.__futter = pos
    def setColor(self, colors):
        self.__bgColor       = colors["bg"]
        self.__futterColor   = colors["futter"]
        self.__schlangeColor = colors["schlange"]

    def paintEvent(self, event):
        self.__bereich = QtCore.QRect(0, 0, self.__size[0], self.__size[1])

        paint = QtGui.QPainter(self)

        paint.setBrush(QtGui.QBrush(QtCore.Qt.SolidPattern))
        paint.setRenderHint(QtGui.QPainter.Antialiasing)
        paint.eraseRect(self.__bereich)
        self.malen(paint)

    def malen(self,paint):
        paint.setPen(self.__bgColor)
        paint.setBrush(self.__bgColor)
        paint.drawRect(self.__bereich)

        paint.setPen(self.__schlangeColor)
        paint.setBrush(self.__schlangeColor)
        x = self.__pos[0]
        y = self.__pos[1]
        radius = self.__radius

        for i in range(len(self.__spielfeld)):
            for j in range(len(self.__spielfeld[i])):
                if self.__spielfeld[i][j] > 0 and (i!=x or j!=y):
                    self.__malQuadrat(paint, i, j, radius)
        self.__malDreieck(paint, x, y, radius, self.__orientierung)

        paint.setPen(self.__futterColor)
        paint.setBrush(self.__futterColor)
        self.__malKreis(paint, self.__futter[0], self.__futter[1], radius/2)

    def __malKreis(self, paint, x, y, r):
        """zeichnet einen Kreis um x,y mit Radius r auf paint"""
        dx = self.__dF[0]
        dy = self.__dF[1]
        paint.drawChord((x+1)*dx-r, (y+1)*dy-r, 2*r, 2*r, 0, 16 * 360)

    def __malQuadrat(self, paint, x, y, a):
        """zeichnet ein Quadrat um x,y mit Seitenlänge a auf paint"""
        dx = self.__dF[0]
        dy = self.__dF[1]
        paint.drawRect((x+1)*dx-a/2, (y+1)*dy-a/2, a, a)

    def __malDreieck(self, paint, x, y, h, richtung):
        """zeichnet ein gleichseitiges Dreieck um x,y mit Höhe h und
        Grundseite g = 2*h, dessen Spitze nach richtung zeigt"""
        dx = self.__dF[0]
        dy = self.__dF[1]

        # Code für rechts
        a = [-h,  h, -h]
        b = [-h,  0,  h]

        if richtung == self.richtungen["rechts"]:
            pass
        elif richtung == self.richtungen["links"]:
            a = [-i for i in a]
        elif richtung == self.richtungen["oben"]:
            a, b = b, a
            b = [-i for i in b]
        elif richtung == self.richtungen["unten"]:
            a, b = b, a

        point1 = QtCore.QPointF((x+1)*dx+a[0], (y+1)*dy+b[0])
        point2 = QtCore.QPointF((x+1)*dx+a[1], (y+1)*dy+b[1])
        point3 = QtCore.QPointF((x+1)*dx+a[2], (y+1)*dy+b[2])
        paint.drawPolygon(point1, point2, point3)
