#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
import random
import sys
from snakeLogik import *
from colorSelektor import *
from zahlSelektor import *
from highscore import *

# TODO: Autopilot
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

        iconSize = QtGui.QIcon('size.png')
        sizeAction = QtGui.QAction(iconSize, '&Size', self)
        #~ sizeAction.setShortcut('Ctrl+L')
        sizeAction.setStatusTip('verändere Spielgeschwindigkeit')
        sizeAction.triggered.connect(self.setSize)

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
        menuFkt.addAction(sizeAction)
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

    def setSize(self):
        self.anzeige.setPause(True)
        sizeChooser = ZweiZahlSelektor(self.anzeige.getSize())
        self.connect(sizeChooser, QtCore.SIGNAL('signalSizeChanged'), self.anzeige.setSize)
        sizeChooser.exec_()
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
