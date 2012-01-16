#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
import random
import sys
from snakeLogik import *
from colorSelektor import *
from zahlSelektor import *
from highscore import *

# TODO: Menüpuznkt wieviel Futter erzeugt werden soll
# TODO: Anzeige benötigte Zeit (über schritte)
# TODO: Anzeige Länge

class SnakeWindow(QtGui.QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Fenstereigenschaften
        self.setWindowTitle('Snake')
        self.setWindowIcon(QtGui.QIcon('icons/icon.png'))

        self.makeMenu()

        self.anzeige = Snake()
        self.setCentralWidget(self.anzeige)
        self.show()

    def keyPressEvent(self, event):
        # weiterleitung der key events an das anzeige/ steuerungswidget
        self.anzeige.keyPressEvent(event)

    def makeMenu(self):
        iconColor = QtGui.QIcon('icons/color.png')
        setColorAction = QtGui.QAction(iconColor, '&Farbe', self)
        setColorAction.setShortcut('c')
        setColorAction.setCheckable(False)
        setColorAction.triggered.connect(self.setColor)

        iconLevel = QtGui.QIcon('icons/level.png')
        levelAction = QtGui.QAction(iconLevel, '&Level', self)
        levelAction.setShortcut('Ctrl+L')
        levelAction.setStatusTip('verändere Spielgeschwindigkeit')
        levelAction.triggered.connect(self.setLevel)

        iconSize = QtGui.QIcon('icons/size.png')
        sizeAction = QtGui.QAction(iconSize, '&Size', self)
        #~ sizeAction.setShortcut('Ctrl+L')
        sizeAction.setStatusTip('verändere Spielgeschwindigkeit')
        sizeAction.triggered.connect(self.setSize)

        iconNeustart = QtGui.QIcon('icons/neustart.png')
        neustartAction = QtGui.QAction(iconNeustart, '&neustart', self)
        neustartAction.setShortcut('Ctrl+N')
        neustartAction.setStatusTip('beginne neue Runde')
        neustartAction.triggered.connect(self.restart)

        iconShowHighscore = QtGui.QIcon('icons/highscore.png')
        showHighscoreAction = QtGui.QAction(iconShowHighscore, '&Highscore', self)
        showHighscoreAction.setShortcut('Ctrl+H')
        showHighscoreAction.setStatusTip('Highscore anzeigen')
        showHighscoreAction.triggered.connect(self.showHighscore)

        iconAutopilot = QtGui.QIcon('icons/autopilot.png')
        autopilotAction = QtGui.QAction(iconAutopilot, '&Autopilot', self)
        autopilotAction.setShortcut('Ctrl+A')
        autopilotAction.setStatusTip('Autopilot aktivieren')
        autopilotAction.setCheckable(True)
        autopilotAction.triggered.connect(self.toggleAutopilot)

        iconAutopilot = QtGui.QIcon('icons/autopilot.png')
        autopilotKonservativAction = QtGui.QAction(iconAutopilot, '&Konservativ', self)
        #~ autopilotKonservativAction.setShortcut('Ctrl+A')
        autopilotKonservativAction.setStatusTip('Konservative KI, perfektes, langsames Spiel')
        autopilotKonservativAction.setCheckable(True)
        autopilotKonservativAction.triggered.connect(self.setAutoKonservativ)

        iconAutopilot = QtGui.QIcon('icons/autopilot.png')
        autopilotTreppeAction = QtGui.QAction(iconAutopilot, '&Treppe', self)
        #~ autopilotTreppeAction.setShortcut('Ctrl+A')
        autopilotTreppeAction.setStatusTip('Treppefreudige KI')
        autopilotTreppeAction.setCheckable(True)
        autopilotTreppeAction.triggered.connect(self.setAutoTreppe)

        iconAutopilot = QtGui.QIcon('icons/autopilot.png')
        autopilotRisikoAction = QtGui.QAction(iconAutopilot, '&Risiko', self)
        #~ autopilotRisikoAction.setShortcut('Ctrl+A')
        autopilotRisikoAction.setStatusTip('Risikofreudige KI')
        autopilotRisikoAction.setCheckable(True)
        autopilotRisikoAction.triggered.connect(self.setAutoRisiko)

        autoKI = QtGui.QActionGroup(self)
        autopilotRisikoAction.setChecked(True)
        autoKI.addAction(autopilotRisikoAction)
        autoKI.addAction(autopilotKonservativAction)
        autoKI.addAction(autopilotTreppeAction)

        iconExit = QtGui.QIcon('icons/exit.png')
        exitAction = QtGui.QAction(iconExit, '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(QtGui.qApp.quit)

        menubar = QtGui.QMenuBar(self)
        menuFkt = menubar.addMenu('Funktion')
        menuDar = menubar.addMenu('Darstellung')
        menuAut = menubar.addMenu('Autopilot')

        menuFkt.addAction(neustartAction)
        menuFkt.addAction(levelAction)
        menuFkt.addAction(sizeAction)
        menuFkt.addAction(showHighscoreAction)
        menuFkt.addAction(exitAction)

        menuDar.addAction(setColorAction)

        menuAut.addAction(autopilotAction)
        menuAut.addSeparator()
        menuAut.addAction(autopilotRisikoAction)
        menuAut.addAction(autopilotKonservativAction)
        menuAut.addAction(autopilotTreppeAction)

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

    def toggleAutopilot(self):
        self.anzeige.toggleAutopilot()

    def setAutoRisiko(self):
        self.anzeige.setAutoRisiko()

    def setAutoKonservativ(self):
        self.anzeige.setAutoKonservativ()

    def setAutoTreppe(self):
        self.anzeige.setAutoTreppe()

def main():
    app = QtGui.QApplication(sys.argv)
    ex = SnakeWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
