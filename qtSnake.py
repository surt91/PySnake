#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
import random
import sys
from colorSelektor import *
from zahlSelektor import *
from highscore import *

# TODO: Menüpunkt zur Anpassung der Spielfeldgröße

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
    def setSpielfeld(self, f):
        self.__spielfeld = f
    def setFutter(self, pos):
        self.__futter = pos
    def setColor(self, colors):
        self.__bgColor          = colors["bg"]
        self.__futterColor      = colors["futter"]
        self.__schlangeColor    = colors["schlange"]

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
        self.__bVerloren = False
        self.__setPunkte(0)

        self.setPause(True)
        self.__block = False

        self.__spielfeld = [[0 for j in range(self.__maxF[1])] for i in range(self.__maxF[0])]

        startF  = [i//2 for i in self.__maxF]

        self.__length = 3

        self.__spielfeld[startF[0]][startF[1]] = self.__length

        self.__orientierung = self.richtungen["oben"]

        self.__pos = startF

        self.__futter = (random.randint(0,self.__maxF[0]-1), random.randint(0,self.__maxF[1]-1))

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
            if self.__orientierung == self.richtungen["oben"]:
                self.__pos[1] -= 1
            elif self.__orientierung == self.richtungen["unten"]:
                self.__pos[1] += 1
            elif self.__orientierung == self.richtungen["links"]:
                self.__pos[0] -= 1
            elif self.__orientierung == self.richtungen["rechts"]:
                self.__pos[0] += 1
            self.__block = False

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
            if self.__spielfeld[i][j] == 0:
                break
        self.__futter = (i,j)

    def __setPunkte(self, p, add = False):
        if add:
            self.__punkte += p
        else:
            self.__punkte = p
        self.punktAnzeige.setText("Punkte: " + "{:04d}".format(self.__punkte))

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
        self.pauseAnzeige.setText("Verloren!")
        if CheckHighscore.getPunkte() < self.__punkte\
                        or CheckHighscore.getLength() < 10:
            hs = SetHighscore(self.__punkte, self.__level)
            hs2 = ShowHighscore()
            hs2.exec_()

    def __ende(self):
        sys.exit()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.__ende()
        if event.key() == QtCore.Qt.Key_P:
            self.setPause(True)
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

    def setColor(self, colors):
        self.farben = colors
        self.anzeige.setColor(colors)

    def getColor(self):
        return self.farben

class SnakeWindow(QtGui.QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Fenstereigenschaften
        self.setWindowTitle('Snake')
        self.setWindowIcon(QtGui.QIcon('icon.png'))

        self.makeMenu()

        self.anzeige = Snake()
        self.setCentralWidget(self.anzeige)
        self.show()

    def keyPressEvent(self, event):
        # weiterleitung der key events an das anzeige/ steuerungswidget
        self.anzeige.keyPressEvent(event)

    def makeMenu(self):
        iconColor = QtGui.QIcon('color.png')
        setColorAction = QtGui.QAction(iconColor, '&Farbe', self)
        setColorAction.setShortcut('c')
        setColorAction.setCheckable(False)
        setColorAction.triggered.connect(self.setColor)

        iconLevel = QtGui.QIcon('level.png')
        levelAction = QtGui.QAction(iconLevel, '&Level', self)
        levelAction.setShortcut('Ctrl+L')
        levelAction.setStatusTip('verändere Spielgeschwindigkeit')
        levelAction.triggered.connect(self.setLevel)

        iconNeustart = QtGui.QIcon('neustart.png')
        neustartAction = QtGui.QAction(iconNeustart, '&neustart', self)
        neustartAction.setShortcut('Ctrl+N')
        neustartAction.setStatusTip('beginne neue Runde')
        neustartAction.triggered.connect(self.restart)

        iconShowHighscore = QtGui.QIcon('showHighscore.png')
        showHighscoreAction = QtGui.QAction(iconShowHighscore, '&Highscore', self)
        showHighscoreAction.setShortcut('Ctrl+H')
        showHighscoreAction.setStatusTip('Highscore anzeigen')
        showHighscoreAction.triggered.connect(self.showHighscore)

        iconExit = QtGui.QIcon('exit.png')
        exitAction = QtGui.QAction(iconExit, '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(QtGui.qApp.quit)

        menubar = QtGui.QMenuBar(self)
        menuFkt = menubar.addMenu('Funktion')
        menuDar = menubar.addMenu('Darstellung')

        menuFkt.addAction(neustartAction)
        menuFkt.addAction(levelAction)
        menuFkt.addAction(showHighscoreAction)
        menuFkt.addAction(exitAction)

        menuDar.addAction(setColorAction)

        self.setMenuBar(menubar)

    def restart(self):
        self.anzeige.neustart()

    def setLevel(self):
        self.anzeige.setPause(True)
        levelChooser = ZahlSelektor(self.anzeige.getLevel())
        self.connect(levelChooser, QtCore.SIGNAL('signalLevelChanged'), self.anzeige.setLevel)
        levelChooser.exec_()
        self.anzeige.neustart()

    def setColor(self):
        self.anzeige.setPause(True)
        colorChooser = ColorSelektor(self.anzeige.getColor())
        self.connect(colorChooser, QtCore.SIGNAL('signalColorChanged'), self.anzeige.setColor)
        colorChooser.exec_()

    def showHighscore(self):
        self.anzeige.setPause(True)
        hs = ShowHighscore()
        hs.exec_()

def main():
    app = QtGui.QApplication(sys.argv)
    ex = SnakeWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
