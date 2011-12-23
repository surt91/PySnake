#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
import os
import time

class ShowHighscore(QtGui.QDialog):
    def __init__(self):
        super().__init__()

        self.hsFileName = os.path.expanduser("~/.qtPySnake")

        self.initUI()

    def initUI(self):
        grid = QtGui.QGridLayout()
        liste = []

        btn = QtGui.QPushButton('&Schließen!', self)
        btn.clicked.connect(self.close)
        btn.setToolTip('Klicke hier um dieses Fenster zu schließen')
        btn.setMaximumSize(btn.sizeHint())
        btn.setDefault(True)

        # header
        header = ["#", "Name", "Level", "Punkte", "Datum"]
        for j in range(len(header)):
            grid.addWidget(QtGui.QLabel(header[j]), 0, j)

        # data
        n = 1
        for i in self.__getData():
            n+=1
            grid.addWidget(QtGui.QLabel("{:2d}. ".format(n-1)), n, 0)
            for j in range(len(i)):
                grid.addWidget(QtGui.QLabel(i[j]), n, j+1)

        # footer
        grid.addWidget(btn, n+1, len(header))

        self.setLayout(grid)

    def __getData(self):
        try:
            hsFile = open(self.hsFileName, "r")
        except IOError:
            return [["Abe", "12", "666", "2011-10-20T19:42"]]
        out = hsFile.readlines()
        hsFile.close()
        for i in range(len(out)):
            if out[i].strip() == "":
                del out[i]
            else:
                out[i] = out[i].strip().split(";")
                out[i][-1] = self.__convertDatum(out[i][-1])
        return out

    def __convertDatum(self, d):
        datum, zeit = d.split("T")
        jahr, monat, tag = datum.split("-")
        return "{} am {}.{}.{}".format(zeit, tag, monat, jahr)

class SetHighscore(QtGui.QDialog):
    def __init__(self, punkte, level):
        super().__init__()

        self.hsFileName = os.path.expanduser("~/.qtPySnake")

        self.level = level
        self.punkte = punkte
        self.datum = self.__getDatum()

        self.initUI()

    def initUI(self):
        self.__nameInput = QtGui.QLineEdit()

        btn = QtGui.QPushButton('&Abschicken!', self)
        btn.clicked.connect(self.__abschicken)
        btn.setToolTip('Klicke hier um deinen Highscore einzutragen')
        btn.setMaximumSize(btn.sizeHint())
        btn.setDefault(True)

        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(self.__nameInput)
        hbox.addWidget(btn)

        self.setLayout(hbox)

        self.exec_()

    def __abschicken(self):
        name = self.__checkString(self.__getTextFromNameInput())
        out = self.__makeString(name, self.punkte, self.level, self.datum)
        self.__saveHS(out)
        self.close()

    def __getTextFromNameInput(self):
        return self.__nameInput.text()

    def __checkString(self, string):
        """entfernt alle nicht alphanumerischen Zeichen aus string"""
        lower = "abcdefghijklmnopqrstuvwxyz"
        upper = lower.upper()
        digit = "0123456789:-"
        alphanumeric = lower + upper + digit
        newString = ""
        for a in string:
            if a in alphanumeric:
                newString += a
        if newString == "":
            newString = "default"
        return newString

    def __getDatum(self):
        t = time.localtime()
        return "{}-{}-{}T{}:{}".format(t.tm_year, t.tm_mon, t.tm_mday,\
                                        t.tm_hour, t.tm_min)

    def __makeString(self, name, punkte, level, datum):
        return "{};{};{};{}\n".format(name, level, punkte, datum)

    def __saveHS(self, string):
        try:
            hsFile = open(self.hsFileName, "r")
            out = hsFile.readlines()
            hsFile.close()
        except IOError:
            out=[]

        fertig = False
        for i in range(len(out)):
            if int(out[i].split(";")[2]) < self.punkte and not fertig:
                fertig = True
                out.insert(i, string)
        if not fertig:
            out.append(string)
        if len(out)>10:
            del out[-1]

        outputString = ""
        for i in out:
            outputString += i

        outfile = open(self.hsFileName, "w")
        outfile.write(outputString)
        outfile.close()

class CheckHighscore():
    def getPunkte():
        hsFileName = os.path.expanduser("~/.qtPySnake")
        try:
            hsFile = open(hsFileName, "r")
        except IOError:
            return 0
        out = hsFile.readlines()
        hsFile.close()
        for i in range(len(out)):
            if out[i].strip() == "":
                del out[i]
            else:
                out[i] = int(out[i].strip().split(";")[2])
        try:
            return min(out)
        except ValueError:
            return 0

    def getLength():
        hsFileName = os.path.expanduser("~/.qtPySnake")
        try:
            hsFile = open(hsFileName, "r")
        except IOError:
            return 0
        out = hsFile.readlines()
        hsFile.close()
        for i in range(len(out)):
            if out[i].strip() == "":
                del out[i]
            #~ else:
                #~ out[i] = int(out[i].strip().split(";")[2])
        return len(out)
