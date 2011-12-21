#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore

class ColorSelektor(QtGui.QDialog):
    def __init__(self, default):
        super().__init__()

        self.__colors = default
        self.initUI()

    def initUI(self):
        self.btnBG = QtGui.QPushButton(self)
        self.btnBG.clicked.connect(self.__setBG)
        self.makeIcon(self.__colors["bg"], self.btnBG)
        labelBG = QtGui.QLabel('Hintergrund', self)

        self.btnF  = QtGui.QPushButton(self)
        self.btnF.clicked.connect(self.__setF)
        self.makeIcon(self.__colors["futter"], self.btnF)
        labelF = QtGui.QLabel('Futter', self)

        self.btnS    = QtGui.QPushButton(self)
        self.btnS.clicked.connect(self.__setS)
        self.makeIcon(self.__colors["schlange"], self.btnS)
        labelS = QtGui.QLabel('Schlange', self)

        hboxBG = QtGui.QHBoxLayout()
        hboxBG.addWidget(self.btnBG)
        hboxBG.addWidget(labelBG)
        hboxBG.addStretch(1)

        hboxS = QtGui.QHBoxLayout()
        hboxS.addWidget(self.btnS)
        hboxS.addWidget(labelS)
        hboxS.addStretch(1)

        hboxF = QtGui.QHBoxLayout()
        hboxF.addWidget(self.btnF)
        hboxF.addWidget(labelF)
        hboxF.addStretch(1)

        btn = QtGui.QPushButton('Anwenden!', self)
        btn.clicked.connect(self.__sendVal)
        btn.setToolTip('Klicke hier um die neuen Farben abzuschicken')
        btn.setMaximumSize(btn.sizeHint())

        vbox1 = QtGui.QVBoxLayout()
        vbox1.addLayout(hboxBG)
        vbox1.addLayout(hboxS)
        vbox1.addLayout(hboxF)

        vbox2 = QtGui.QVBoxLayout()
        vbox2.addStretch(1)
        vbox2.addWidget(btn)

        hbox = QtGui.QHBoxLayout()
        hbox.addLayout(vbox1)
        hbox.addLayout(vbox2)

        self.setLayout(hbox)

        self.setWindowTitle('Farb Auswahl')

        self.show()

    def makeIcon(self, color, button):
        x = QtGui.QPixmap(100,100)
        x.fill(color)
        button.setIcon(QtGui.QIcon(x))

    def __setBG(self):
        self.__colors['bg'] = self.__setColor()
        self.makeIcon(self.__colors["bg"], self.btnBG)

    def __setS(self):
        self.__colors['schlange'] = self.__setColor()
        self.makeIcon(self.__colors["schlange"], self.btnS)

    def __setF(self):
        self.__colors['futter'] = self.__setColor()
        self.makeIcon(self.__colors["futter"], self.btnF)

    def __setColor(self):
        return QtGui.QColorDialog.getColor()

    def __sendVal(self):
        self.emit(QtCore.SIGNAL('signalColorChanged'), self.__colors)
        self.close()
