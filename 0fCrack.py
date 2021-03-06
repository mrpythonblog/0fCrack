# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pdfcracker.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

# Github : https://github.com/mrpythonblog

##########################################
#    
#########       0fCrack       ############     
#          
##########################################

import argparse
import progressbar
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow
from pikepdf import open as openpdf
import sys
from os import path
from pikepdf._qpdf import PasswordError
from rarfile import RarFile,BadRarFile
from py7zr import SevenZipFile
from _lzma import LZMAError # Seven Zip Files BAD Password ERROR .
from zipfile import ZipFile

file_signs = {"255044462d" : "PDF" , "526172211a07" : "RAR" , "377abcaf271c" : "7Z", "504b" : "ZIP"} # All Signs with Small Letters .

class Main(object):
    def setupUi(self, MainWindow):
        self.guimode = True
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(552, 428)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.open1 = QtWidgets.QPushButton(self.centralwidget)
        self.open1.setGeometry(QtCore.QRect(440, 20, 91, 51))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.open1.setFont(font)
        self.open1.setObjectName("open1")
        self.open1.clicked.connect(self.open1Action)
        self.entry1 = QtWidgets.QLineEdit(self.centralwidget)
        self.entry1.setGeometry(QtCore.QRect(20, 20, 411, 51))
        self.entry1.setReadOnly(True)
        self.entry1.setStyleSheet("background : rgb(230, 255, 245)")
        self.entry1.setObjectName("entry1")
        self.open2 = QtWidgets.QPushButton(self.centralwidget)
        self.open2.setGeometry(QtCore.QRect(440, 80, 91, 51))
        self.open2.clicked.connect(self.open2Action)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.open2.setFont(font)
        self.open2.setObjectName("open2")
        self.entry2 = QtWidgets.QLineEdit(self.centralwidget)
        self.entry2.setGeometry(QtCore.QRect(20, 80, 411, 51))
        self.entry2.setStyleSheet("background : rgb(230, 255, 245)")
        self.entry2.setInputMask("")
        self.entry2.setText("")
        self.entry2.setObjectName("entry2")
        self.entry2.setReadOnly(True)
        self.passwordListWidget = QtWidgets.QListWidget(self.centralwidget)
        self.passwordListWidget.setGeometry(QtCore.QRect(20, 170, 411, 181))
        self.passwordListWidget.setStyleSheet("background : rgb(160, 255, 155)")
        self.passwordListWidget.setObjectName("passwordListWidget")
        self.attackButton = QtWidgets.QPushButton(self.centralwidget)
        self.attackButton.setGeometry(QtCore.QRect(440, 170, 91, 181))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.attackButton.setFont(font)
        self.attackButton.setStyleSheet("background : rgb(255, 0, 4)")
        self.attackButton.setObjectName("attackButton")
        self.attackButton.clicked.connect(self.attackButtonAction)
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setEnabled(True)
        self.progressBar.setGeometry(QtCore.QRect(20, 370, 511, 31))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.progressBar.setFont(font)
        self.progressBar.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setEnabled(True)
        self.label.setGeometry(QtCore.QRect(20, 140, 501, 19))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.label.setFont(font)
        self.label.setText("")
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
    def setupConsole(self , file , passwordlist):
        self.file = file
        self.passwordlist = passwordlist
        self.guimode = False

        if self.passwordlist and self.file and path.isfile(self.passwordlist) and path.isfile(self.file):
            # everything is ok ...
            # Detect The File Type Using File Signuture
            self.n = len(open(self.passwordlist).readlines())
            widgets = ["Cracking : " , progressbar.Bar("▇") , progressbar.Counter(format = "[ %d / {} ]".format(self.n))]
            self.bar = progressbar.ProgressBar(maxval=self.n , widgets = widgets).start()
            file_type = ""
            file = open(self.file , "rb")
            sign = file.read()[0:20].hex()
            file.close()
            for item in file_signs:
                if item in sign:
                    file_type = file_signs[item]

            if file_type == "PDF":
                password = self.pdfCrackAction()
                if password:
                    print("\n\n[[ Password :‌ {} ]]".format(password))
                else:
                    print("Password Not Found !")
            if file_type == "ZIP":
                password = self.ZipCrackAction()
                if password:
                    print("\n\n[[ Password :‌ {} ]]".format(password))
                else:
                    print("Password Not Found !")
            if file_type == "RAR":
                password = self.rarCrackAction()
                if password:
                    print("\n\n[[ Password :‌ {} ]]".format(password))
                else:
                    print("Password Not Found !")
            if file_type == "7Z":
                password = self.sevenZipCrackAction()
                if password:
                    print("\n\n[[ Password :‌ {} ]]".format(password))
                else:
                    print("Password Not Found !")

        

    def open1Action(self):
        file, _ = QtWidgets.QFileDialog.getOpenFileName(MainWindow , "Open File" , "Select File To Crack" , "All Files (*)")
        if file:
            self.file = file
            self.entry1.setText(self.file)
    def open2Action(self):
        passwordlist, _ = QtWidgets.QFileDialog.getOpenFileName(MainWindow , "Open File" , "Select Password List" , "All Files (*)")
        if passwordlist:
            if path.isfile(passwordlist):
                self.passwordlist = passwordlist
                self.entry2.setText(passwordlist)
                passwordlist = open(passwordlist,"r")
                self.n = 0
                self.passwordListWidget.clear() # Clear Items of Password List Widget
                for password in passwordlist:
                    password = password.strip("\n")
                    self.passwordListWidget.addItem(password)
                    self.n += 1
                passwordlist.close()
                self.label.setText("{} Passwords Loaded . Ready To Attack !".format(self.n))
    def attackButtonAction(self):
        if ("passwordlist" not in dir(self)) or ("file" not in dir(self)):
            msg = QtWidgets.QMessageBox.information(MainWindow , "ERROR" , "please select both File and Password List !" , QtWidgets.QMessageBox.Ok)
            del msg
            return
        if self.passwordlist and self.file and path.isfile(self.passwordlist) and path.isfile(self.file):
            # everything is ok ...
            # Detect The File Type Using File Signuture
            file_type = ""
            file = open(self.file , "rb")
            sign = file.read()[0:20].hex()
            file.close()
            for item in file_signs:
                if item in sign:
                    file_type = file_signs[item]
            if file_type == "PDF":
                password = self.pdfCrackAction()
                if password:
                    msg = QtWidgets.QMessageBox.information(MainWindow , "Password Cracked" , "Password : {}".format(password) , QtWidgets.QMessageBox.Ok)
                    del msg
                    return
                else:
                    msg = QtWidgets.QMessageBox.information(MainWindow , "Password Not Found !" , "Password Not Found in your Password List" , QtWidgets.QMessageBox.Ok)
                    del msg
                    return
            elif file_type == "RAR":
                # Rar Cracking
                password = self.rarCrackAction()
                if password:
                    msg = QtWidgets.QMessageBox.information(MainWindow , "Password Cracked" , "Password : {}".format(password) , QtWidgets.QMessageBox.Ok)
                    del msg
                    self.progressBar.setProperty('value' , 0)
                    return
                else:
                    msg = QtWidgets.QMessageBox.information(MainWindow , "Password Not Found !" , "Password Not Found in your Password List" , QtWidgets.QMessageBox.Ok)
                    del msg
                    self.progressBar.setProperty('value' , 0)
                    return
            elif file_type == "7Z":
                ## 7z Cracking 
                password = self.sevenZipCrackAction()
                if password:
                    msg = QtWidgets.QMessageBox.information(MainWindow , "Password Cracked" , "Password : {}".format(password) , QtWidgets.QMessageBox.Ok)
                    del msg
                    self.progressBar.setProperty('value' , 0)
                    return
                else:
                    msg = QtWidgets.QMessageBox.information(MainWindow , "Password Not Found !" , "Password Not Found in your Password List" , QtWidgets.QMessageBox.Ok)
                    del msg
                    self.progressBar.setProperty('value' , 0)
                    return
            elif file_type == "ZIP":
                ##‌ ZIP Cracking
                password = self.ZipCrackAction()
                if password:
                    msg = QtWidgets.QMessageBox.information(MainWindow , "Password Cracked" , "Password : {}".format(password) , QtWidgets.QMessageBox.Ok)
                    del msg
                    self.progressBar.setProperty('value' , 0)
                    return
                else:
                    msg = QtWidgets.QMessageBox.information(MainWindow , "Password Not Found !" , "Password Not Found in your Password List" , QtWidgets.QMessageBox.Ok)
                    del msg
                    self.progressBar.setProperty('value' , 0)
                    return

            else:
                msg = QtWidgets.QMessageBox.information(MainWindow , "ERROR" , "I Can't Crack This File Type" , QtWidgets.QMessageBox.Ok)
                del msg
                return 
            
        msg = QtWidgets.QMessageBox.information(MainWindow , "ERROR" , "Bad File Or PasswordList !" , QtWidgets.QMessageBox.Ok)
        del msg


        
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle("0fCrack GUI")
        self.open1.setText(_translate("MainWindow", "OPEN"))
        self.entry1.setPlaceholderText(_translate("MainWindow", "Open PDF File ...."))
        self.open2.setText(_translate("MainWindow", "OPEN"))
        self.entry2.setPlaceholderText(_translate("MainWindow", "Open Password List File ...."))
        self.attackButton.setText(_translate("MainWindow", "ATTACK"))
    
    def pdfCrackAction(self):
        progressBarValue = 0
        tested = 0
        for password in open(self.passwordlist):
            try:
                app.processEvents() # Process Events when 0fCrack is Cracking ...
            except :
                pass # Process Events when 0fCrack is Cracking ...
            password = password.strip("\n")
            try:
                openpdf(self.file , password)
                return password
            except PasswordError:
                tested += 1
                if self.guimode:
                    self.progressBar.setProperty("value" , (tested * 100) / self.n)
                else:
                    self.bar.update(tested)
        return False
    
    def rarCrackAction(self):
        progressBarValue = 0
        tested = 0
        rar = RarFile(self.file)
        for password in open(self.passwordlist):
            try:
                app.processEvents() # Process Events when 0fCrack is Cracking ...
            except :
                pass # Process Events when 0fCrack is Cracking ...
            password = password.strip("\n")
            try:
                rar.testrar(password)
                return password
            except BadRarFile:
                tested += 1
                if self.guimode:
                    self.progressBar.setProperty("value" , (tested * 100) / self.n)
                else:
                    self.bar.update(tested)
        return False
    def sevenZipCrackAction(self):
        progressBarValue = 0
        tested = 0
        for password in open(self.passwordlist):
            try:
                app.processEvents() # Process Events when 0fCrack is Cracking ...
            except :
                pass
            password = password.strip("\n")
            file = SevenZipFile(self.file , mode = "r" , password = password)
            try:
                file.testzip()
                return password
            except LZMAError:
                tested += 1
                if self.guimode:
                    self.progressBar.setProperty("value" , (tested * 100) / self.n)
                else:
                    self.bar.update(tested)
            except EOFError:
                tested += 1
                if self.guimode:
                    self.progressBar.setProperty("value" , (tested * 100) / self.n)
                else:
                    self.bar.update(tested)
        return False
    def ZipCrackAction(self):
        progressBarValue = 0
        tested = 0
        for password in open(self.passwordlist):
            try:
                app.processEvents() # Process Events when 0fCrack is Cracking ...
            except :
                pass
            password = password.strip("\n")
            try:
                file = ZipFile(self.file)
                file.extractall(pwd = password.encode())
                return password
            except:
                tested += 1
                if self.guimode:
                    self.progressBar.setProperty("value" , (tested * 100) / self.n)
                else:
                    self.bar.update(tested)
        return False


            
            


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f" , "--file" , metavar="FILE" , help="File To Crack")
    parser.add_argument("-p" , "--passwordlist" , metavar="PassList" , help="Password List For Crack")
    args = parser.parse_args()

    if args.file and args.passwordlist:
        main = Main()
        main.setupConsole(args.file , args.passwordlist)
    else:
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        main = Main()
        main.setupUi(MainWindow)
        MainWindow.show()
        sys.exit(app.exec_())
