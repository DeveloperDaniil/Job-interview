import ctypes

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QPalette, QBrush, QPixmap, QFont, QImage, QIcon
from PyQt5.QtWidgets import QMainWindow

from Questions import Questions

myAppId = 'mycompany.myproduct.subproduct.version'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myAppId)


class Ui_Dialog(object):
    def setupUi(self, Dialog, topic):
        Dialog.setObjectName("Dialog")
        Dialog.setMinimumSize(1024, 768)
        if topic == "white":
            palette = QPalette()
            palette.setBrush(QPalette.Background, QBrush(QPixmap("images/white_background.jpg")))
            Dialog.setPalette(palette)
        else:
            palette = QPalette()
            palette.setBrush(QPalette.Background, QBrush(QPixmap("images/black_background.jpg")))
            Dialog.setPalette(palette)
        self.ButtonNext = QtWidgets.QPushButton(Dialog)
        self.ButtonNext.setGeometry(QtCore.QRect(370, 680, 301, 51))
        self.ButtonNext.setObjectName("ButtonNext")
        self.ButtonNext.setFont(QFont('Century Gothic', 10))
        self.dateEdit = QtWidgets.QDateEdit(Dialog)
        self.dateEdit.setGeometry(QtCore.QRect(200, 111, 271, 31))
        self.dateEdit.setObjectName("dateEdit")
        self.dateEdit.setFont(QFont('Century Gothic', 10))
        self.labelT = QtWidgets.QLabel(Dialog)
        self.labelT.setGeometry(QtCore.QRect(20, 10, 171, 31))
        self.labelT.setObjectName("labelT")
        self.labelT.setFont(QFont('Century Gothic', 9))
        self.lineEditTitle = QtWidgets.QLineEdit(Dialog)
        self.lineEditTitle.setGeometry(QtCore.QRect(200, 10, 271, 31))
        self.lineEditTitle.setObjectName("lineEditTitle")
        self.labelN = QtWidgets.QLabel(Dialog)
        self.labelN.setGeometry(QtCore.QRect(20, 60, 171, 31))
        self.labelN.setObjectName("labelN")
        self.labelN.setFont(QFont('Century Gothic', 9))
        self.lineEditName = QtWidgets.QLineEdit(Dialog)
        self.lineEditName.setGeometry(QtCore.QRect(200, 60, 271, 31))
        self.lineEditName.setObjectName("lineEditName")
        self.labelD = QtWidgets.QLabel(Dialog)
        self.labelD.setGeometry(QtCore.QRect(20, 110, 171, 31))
        self.labelD.setObjectName("labelD")
        self.labelD.setFont(QFont('Century Gothic', 7))
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.ButtonNext.setText(_translate("Dialog", "Далее"))
        self.labelT.setText(_translate("Dialog", "Название компании"))
        self.labelN.setText(_translate("Dialog", "ФИО кандидата"))
        self.labelD.setText(_translate("Dialog", "Дата рождения кандидата"))


class Registration(QMainWindow, Ui_Dialog):
    resized = QtCore.pyqtSignal()

    def __init__(self, topic, x, y, m, nX, nY):
        super().__init__()
        self.nX, self.nY = nX, nY
        self.topic = topic
        if topic == "white":
            self.im = QImage()
            self.im.load("images/white_background.jpg")
        else:
            self.im = QImage()
            self.im.load("images/black_background.jpg")
        self.setupUi(self, topic)
        self.design()
        self.setWindowTitle('Регистрация')
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

        self.ButtonNext.move(int(self.width() * 0.333), int(self.height() * 0.882))
        self.ButtonNext.setFixedSize(int(self.width() * 0.333), int(self.height() * 0.079))

        return super(Registration, self).resizeEvent(event)

    def logic(self):
        self.ButtonNext.clicked.connect(self.next_window)

    def next_window(self):
        title = self.lineEditTitle.text()
        name = self.lineEditName.text().title()
        birthday = self.dateEdit.text()
        if not title:
            title = 'Company'
        if not name:
            name = 'Candidate'
        data = [title, name, birthday]
        self.close()
        self.w = Questions(self.topic, self.width(), self.height(), self.isMaximized(), data, self.nX, self.nY)
        self.w.show()

    def design(self):
        if self.topic == "white":
            style = 'background: rgb(255,255,255);color: rgb(0,0,0);'
            self.ButtonNext.setStyleSheet(style)
        else:
            style = 'background: rgb(10,10,10);color: rgb(255,255,255); \
                     border-color: rgb(255,255,255);border-style: solid; \
                     border-radius: 4px; border-width: 3px;'
            self.lineEditTitle.setStyleSheet(style)
            self.lineEditName.setStyleSheet(style)
            self.dateEdit.setStyleSheet(style)
            self.ButtonNext.setStyleSheet(style)
            style = 'color: rgb(255,255,255);'
            self.labelT.setStyleSheet(style)
            self.labelN.setStyleSheet(style)
            self.labelD.setStyleSheet(style)
