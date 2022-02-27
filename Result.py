import ctypes
import sys

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QPalette, QBrush, QPixmap, QFont, QImage, QIcon
from PyQt5.QtWidgets import QMainWindow

myAppId = 'mycompany.myproduct.subproduct.version'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myAppId)


class Ui_Dialog(object):
    def setupUi(self, Dialog, topic):
        Dialog.setObjectName("Dialog")
        Dialog.setMinimumSize(1280, 720)
        if topic == "white":
            palette = QPalette()
            palette.setBrush(QPalette.Background, QBrush(QPixmap("images/white_background.jpg")))
            Dialog.setPalette(palette)
        else:
            palette = QPalette()
            palette.setBrush(QPalette.Background, QBrush(QPixmap("images/black_background.jpg")))
            Dialog.setPalette(palette)
        self.labelResult = QtWidgets.QLabel(Dialog)
        self.labelResult.setGeometry(QtCore.QRect(80, 130, 770, 90))
        self.labelResult.setText("")
        self.labelResult.setAlignment(QtCore.Qt.AlignCenter)
        self.labelResult.setObjectName("labelResult")
        self.labelResult.setFont(QFont('Century Gothic', 14))
        self.labelResult.setWordWrap(True)
        self.ButtonEnd = QtWidgets.QPushButton(Dialog)
        self.ButtonEnd.setGeometry(QtCore.QRect(340, 640, 270, 60))
        self.ButtonEnd.setObjectName("ButtonEnd")
        self.ButtonEnd.setFont(QFont('Century Gothic', 18))
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.ButtonEnd.setText(_translate("Dialog", "Закрыть"))


class Result(QMainWindow, Ui_Dialog):
    resized = QtCore.pyqtSignal()

    def __init__(self, topic, x, y, m, mark):
        super().__init__()
        self.topic = topic
        self.mark = mark
        if topic == "white":
            self.im = QImage()
            self.im.load("images/white_background.jpg")
        else:
            self.im = QImage()
            self.im.load("images/black_background.jpg")
        self.setupUi(self, topic)
        self.design()
        self.setWindowTitle('Результат')
        if self.mark == 0:
            self.labelResult.setText("Мне кажется, что этот чувак нам не подходит")
        else:
            self.labelResult.setText(f"Кандидат примерно проработает {self.mark} дней")
        if m:
            self.showMaximized()
        else:
            self.resize(x, y)
        self.setWindowIcon(QIcon('images/icon.png'))
        self.logic()

    def resize_image(self):
        if (self.width() > 2560) or (self.height() > 1440):
            size = (self.width(), self.height())
            imR = self.im.scaled(size[0], size[1])
            palette = QPalette()
            palette.setBrush(QPalette.Background, QBrush(QPixmap(QPixmap.fromImage(imR))))
            self.setPalette(palette)

    def resizeEvent(self, event):
        self.resized.emit()
        self.resize_image()

        self.labelResult.move(int(self.width() / 2) - int(self.labelResult.width() / 2), int(self.height() * 0.169))

        self.ButtonEnd.setFixedSize(int(self.width() * 0.547), int(self.height() * 0.091))
        self.ButtonEnd.move(int(self.width() / 2) - int(self.ButtonEnd.width() / 2), int(self.height() * 0.831))

        return super(Result, self).resizeEvent(event)

    def logic(self):
        self.ButtonEnd.clicked.connect(sys.exit)

    def design(self):
        if self.topic == "white":
            style = 'background: rgb(255,255,255);color: rgb(0,0,0);'
            self.ButtonEnd.setStyleSheet(style)
        else:
            style = 'background: rgb(10,10,10);color: rgb(150,150,150); \
                                 border-color: rgb(50,50,50);border-style: solid; \
                                 border-radius: 4px; border-width: 3px;'
            self.ButtonEnd.setStyleSheet(style)
            style = 'color: rgb(150,150,150)'
            self.labelResult.setStyleSheet(style)
