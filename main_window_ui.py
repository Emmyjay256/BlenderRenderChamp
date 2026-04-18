# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.11.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QLabel, QLineEdit, QListWidget,
    QListWidgetItem, QMainWindow, QMenuBar, QProgressBar,
    QPushButton, QSizePolicy, QStatusBar, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.listQueue = QListWidget(self.centralwidget)
        self.listQueue.setObjectName(u"listQueue")
        self.listQueue.setGeometry(QRect(50, 20, 711, 221))
        self.btnStart = QPushButton(self.centralwidget)
        self.btnStart.setObjectName(u"btnStart")
        self.btnStart.setGeometry(QRect(80, 250, 121, 61))
        self.btnStop = QPushButton(self.centralwidget)
        self.btnStop.setObjectName(u"btnStop")
        self.btnStop.setGeometry(QRect(80, 330, 121, 61))
        self.btnAdd = QPushButton(self.centralwidget)
        self.btnAdd.setObjectName(u"btnAdd")
        self.btnAdd.setGeometry(QRect(300, 250, 121, 61))
        self.btnRemove = QPushButton(self.centralwidget)
        self.btnRemove.setObjectName(u"btnRemove")
        self.btnRemove.setGeometry(QRect(300, 330, 121, 61))
        self.lblStatus = QLabel(self.centralwidget)
        self.lblStatus.setObjectName(u"lblStatus")
        self.lblStatus.setGeometry(QRect(80, 425, 581, 31))
        self.progressBar = QProgressBar(self.centralwidget)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setGeometry(QRect(80, 490, 671, 23))
        self.progressBar.setValue(24)
        self.lineBlenderPath = QLineEdit(self.centralwidget)
        self.lineBlenderPath.setObjectName(u"lineBlenderPath")
        self.lineBlenderPath.setGeometry(QRect(80, 520, 631, 22))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.btnStart.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.btnStop.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
        self.btnAdd.setText(QCoreApplication.translate("MainWindow", u"Add", None))
        self.btnRemove.setText(QCoreApplication.translate("MainWindow", u"Remove", None))
        self.lblStatus.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.lineBlenderPath.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Paste path to blender.exe here...", None))
    # retranslateUi

