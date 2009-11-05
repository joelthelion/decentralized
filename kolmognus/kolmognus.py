# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'KolmoGNUS.ui'
#
# Created: Mon Nov 26 17:42:05 2007
#      by: PyQt4 UI code generator 4.3.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(QtCore.QSize(QtCore.QRect(0,0,800,600).size()).expandedTo(MainWindow.minimumSizeHint()))

        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.GoodBtn = QtGui.QToolButton(self.centralwidget)
        self.GoodBtn.setGeometry(QtCore.QRect(100,10,100,25))
        self.GoodBtn.setObjectName("GoodBtn")

        self.BadBtn = QtGui.QToolButton(self.centralwidget)
        self.BadBtn.setGeometry(QtCore.QRect(210,10,100,25))
        self.BadBtn.setObjectName("BadBtn")

        self.RefreshBtn = QtGui.QPushButton(self.centralwidget)
        self.RefreshBtn.setGeometry(QtCore.QRect(320,10,100,25))
        self.RefreshBtn.setObjectName("RefreshBtn")

        self.RedditBtn = QtGui.QToolButton(self.centralwidget)
        self.RedditBtn.setGeometry(QtCore.QRect(430,10,125,25))
        self.RedditBtn.setObjectName("RedditBtn")

        self.QuitBtn = QtGui.QPushButton(self.centralwidget)
        self.QuitBtn.setGeometry(QtCore.QRect(10,10,80,25))
        self.QuitBtn.setObjectName("QuitBtn")

        self.FeedList = QtGui.QListWidget(self.centralwidget)
        self.FeedList.setGeometry(QtCore.QRect(10,50,781,501))
        self.FeedList.setObjectName("FeedList")
        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0,0,800,25))
        self.menubar.setObjectName("menubar")

        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")

        self.menuTools = QtGui.QMenu(self.menubar)
        self.menuTools.setObjectName("menuTools")

        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.actionAbout = QtGui.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")

        self.actionQuit = QtGui.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")

        self.actionManually_train_filter = QtGui.QAction(MainWindow)
        self.actionManually_train_filter.setObjectName("actionManually_train_filter")

        self.actionShow_filter_info = QtGui.QAction(MainWindow)
        self.actionShow_filter_info.setObjectName("actionShow_filter_info")
        self.menuFile.addAction(self.actionQuit)
        self.menuTools.addAction(self.actionManually_train_filter)
        self.menuTools.addAction(self.actionShow_filter_info)
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.QuitBtn,QtCore.SIGNAL("clicked()"),MainWindow.close)
        QtCore.QObject.connect(self.actionQuit,QtCore.SIGNAL("activated()"),MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "KolmoGNUS - intelligent feed reader", None, QtGui.QApplication.UnicodeUTF8))
        self.GoodBtn.setText(QtGui.QApplication.translate("MainWindow", "Good !", None, QtGui.QApplication.UnicodeUTF8))
        self.GoodBtn.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+L, Ctrl+S", None, QtGui.QApplication.UnicodeUTF8))
        self.BadBtn.setText(QtGui.QApplication.translate("MainWindow", "Bad !", None, QtGui.QApplication.UnicodeUTF8))
        self.BadBtn.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+D", None, QtGui.QApplication.UnicodeUTF8))
        self.RefreshBtn.setText(QtGui.QApplication.translate("MainWindow", "Refresh !", None, QtGui.QApplication.UnicodeUTF8))
        self.RefreshBtn.setShortcut(QtGui.QApplication.translate("MainWindow", "F5", None, QtGui.QApplication.UnicodeUTF8))
        self.RedditBtn.setText(QtGui.QApplication.translate("MainWindow", "Discuss on reddit", None, QtGui.QApplication.UnicodeUTF8))
        self.QuitBtn.setText(QtGui.QApplication.translate("MainWindow", "Quit", None, QtGui.QApplication.UnicodeUTF8))
        self.QuitBtn.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+Q", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(QtGui.QApplication.translate("MainWindow", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.menuTools.setTitle(QtGui.QApplication.translate("MainWindow", "Tools", None, QtGui.QApplication.UnicodeUTF8))
        self.menuHelp.setTitle(QtGui.QApplication.translate("MainWindow", "Help", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAbout.setText(QtGui.QApplication.translate("MainWindow", "About", None, QtGui.QApplication.UnicodeUTF8))
        self.actionQuit.setText(QtGui.QApplication.translate("MainWindow", "Quit", None, QtGui.QApplication.UnicodeUTF8))
        self.actionQuit.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+Q", None, QtGui.QApplication.UnicodeUTF8))
        self.actionManually_train_filter.setText(QtGui.QApplication.translate("MainWindow", "Manually train filter", None, QtGui.QApplication.UnicodeUTF8))
        self.actionShow_filter_info.setText(QtGui.QApplication.translate("MainWindow", "Show filter info", None, QtGui.QApplication.UnicodeUTF8))

