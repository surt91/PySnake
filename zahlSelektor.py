#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore

class ZahlSelektor(QtGui.QDialog):
    def __init__(self, default):
        super().__init__()

        self.initUI(default)

    def initUI(self, default):
        lcd = QtGui.QLCDNumber(self)
        sld = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        sld.setRange(1,15)
        sld.setTracking(True)

        sld.setValue(default)
        lcd.display(default)
        self.__wert = default

        sld.valueChanged.connect(lcd.display)
        sld.valueChanged.connect(self.__setVal)

        btn = QtGui.QPushButton('&Setzen!', self)
        btn.clicked.connect(self.__sendVal)
        btn.setToolTip('Klicke hier um die neues Level abzuschicken')
        btn.setMaximumSize(btn.sizeHint())
        btn.setDefault(True)

        vbox1 = QtGui.QVBoxLayout()
        vbox1.addWidget(lcd)
        vbox1.addWidget(sld)

        vbox2 = QtGui.QVBoxLayout()
        vbox2.addStretch(1)
        vbox2.addWidget(btn)

        hbox = QtGui.QHBoxLayout()
        hbox.addLayout(vbox1)
        hbox.addLayout(vbox2)

        self.setLayout(hbox)

        self.setWindowTitle('Level Auswahl')

    def __setVal(self, x):
        self.__wert = x

    def __sendVal(self):
        self.emit(QtCore.SIGNAL('signalLevelChanged'), self.__wert)
        self.close()

class ZweiZahlSelektor(ZahlSelektor):
    def initUI(self, default):
        lcdX = QtGui.QLCDNumber(self)
        sldX = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        sldX.setRange(2,100)
        sldX.setTracking(True)

        lcdY = QtGui.QLCDNumber(self)
        sldY = QtGui.QSlider(QtCore.Qt.Vertical, self)
        sldY.setRange(2,100)
        sldY.setTracking(True)

        sldX.valueChanged.connect(lcdX.display)
        sldX.valueChanged.connect(self.__setValX)
        sldY.valueChanged.connect(lcdY.display)
        sldY.valueChanged.connect(self.__setValY)

        sldX.setValue(default[0])
        sldY.setValue(default[1])
        self.__wert = default

        btn = QtGui.QPushButton('&Setzen!', self)
        btn.clicked.connect(self.__sendVal)
        btn.setToolTip('Klicke hier um die neue Größe abzuschicken')
        btn.setMaximumSize(btn.sizeHint())
        btn.setDefault(True)

        grid = QtGui.QGridLayout()
        grid.addWidget(lcdX, 1, 2)
        grid.addWidget(sldX, 1, 2)

        grid.addWidget(lcdY, 2, 1)
        grid.addWidget(sldY, 2, 1)

        grid.addWidget(btn, 2, 3)

        self.setLayout(grid)

        self.setWindowTitle('Größen Auswahl')

    def __setValX(self, x):
        self.__wertX = x
    def __setValY(self, y):
        self.__wertY = y

    def __sendVal(self):
        self.emit(QtCore.SIGNAL('signalSizeChanged'), (self.__wertX, self.__wertY))
        self.close()

