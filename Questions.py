import ctypes

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QPalette, QBrush, QPixmap, QFont, QImage, QIcon
from PyQt5.QtWidgets import QMainWindow

import Dictionary_Of_Questions
from Neuron import processing
from Result import Result

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
        font = QFont('Century Gothic', 18)
        font.setBold(True)
        self.labelQuestion = QtWidgets.QLabel(Dialog)
        self.labelQuestion.setFont(font)
        self.labelQuestion.setGeometry(QtCore.QRect(330, 20, 700, 41))
        self.labelQuestion.setAlignment(QtCore.Qt.AlignCenter)
        self.labelQuestion.setObjectName("labelQuestion")
        self.labelExplanation1 = QtWidgets.QLabel(Dialog)
        self.labelExplanation1.setGeometry(QtCore.QRect(10, 80, 451, 541))
        self.labelExplanation1.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.labelExplanation1.setObjectName("labelExplanation1")
        self.labelExplanation1.setFont(QFont('Century Gothic', 12))
        self.labelExplanation1.setWordWrap(True)
        self.labelExplanation2 = QtWidgets.QLabel(Dialog)
        self.labelExplanation2.setGeometry(QtCore.QRect(580, 80, 451, 541))
        self.labelExplanation2.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.labelExplanation2.setObjectName("labelExplanation2")
        self.labelExplanation2.setFont(QFont('Century Gothic', 12))
        self.labelExplanation2.setWordWrap(True)
        self.trash = QtWidgets.QLabel(Dialog)
        self.trash.setGeometry(QtCore.QRect(40, 690, 270, 51))
        self.trash.setObjectName("trash")
        self.trash.setFont(QFont('Century Gothic', 10))
        self.spinBoxScore = QtWidgets.QSpinBox(Dialog)
        self.spinBoxScore.setGeometry(QtCore.QRect(320, 700, 91, 31))
        self.spinBoxScore.setMaximum(10)
        self.spinBoxScore.setObjectName("spinBoxScore")
        self.spinBoxScore.setFont(QFont('Century Gothic', 10))
        self.ButtonNext = QtWidgets.QPushButton(Dialog)
        self.ButtonNext.setGeometry(QtCore.QRect(720, 690, 281, 51))
        self.ButtonNext.setObjectName("ButtonNext")
        self.ButtonNext.setFont(QFont('Century Gothic', 10))
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.labelQuestion.setText(_translate("Dialog", ""))
        self.labelExplanation1.setText(_translate("Dialog", ""))
        self.labelExplanation2.setText(_translate("Dialog", ""))
        self.trash.setText(_translate("Dialog", "Оцените кандидата от 0 до 10:"))
        self.ButtonNext.setText(_translate("Dialog", "Следующий вопрос"))


class Questions(QMainWindow, Ui_Dialog):
    resized = QtCore.pyqtSignal()

    def __init__(self, topic, x, y, m, data, nX, nY):
        super().__init__()
        self.nX, self.nY = nX, nY
        self.topic = topic
        self.data = data
        self.dict = Dictionary_Of_Questions.dict
        self.keys = list(self.dict.keys())
        self.i = 0
        self.mark = 0
        if topic == "white":
            self.im = QImage()
            self.im.load("images/white_background.jpg")
        else:
            self.im = QImage()
            self.im.load("images/black_background.jpg")
        self.setupUi(self, topic)
        self.design()
        self.setWindowTitle('Вопрос №1')
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

        self.labelQuestion.move(int(self.width() / 2) - int(self.labelQuestion.width() / 2), self.labelQuestion.y())

        self.labelExplanation1.setFixedSize(int(self.width() * 0.449), int(self.height() * 0.76))

        self.trash.move(self.trash.x(), int(self.height() * 0.8955))

        self.spinBoxScore.move(self.spinBoxScore.x(), int(self.height() * 0.91))

        self.ButtonNext.move(int(self.width() * 0.7), int(self.height() * 0.9))
        self.ButtonNext.setFixedSize(int(self.width() * 0.266), int(self.height() * 0.074))

        self.labelExplanation2.move(int(self.width() * 0.552), self.labelExplanation2.y())
        self.labelExplanation2.setFixedSize(int(self.width() * 0.446), int(self.height() * 0.725))

        return super(Questions, self).resizeEvent(event)

    def logic(self):
        self.labelQuestion.setText(self.keys[self.i])
        self.labelExplanation1.setText(self.dict[self.keys[self.i]][0])
        self.labelExplanation2.setText(self.dict[self.keys[self.i]][1])
        self.ButtonNext.clicked.connect(self.next_question)

    def next_question(self):
        self.i += 1
        self.setWindowTitle(f'Вопрос №{self.i + 1}')
        self.data.append(self.spinBoxScore.value())
        if self.i == len(self.keys):
            mark = processing(self.data, self.nX, self.nY)
            self.close()
            self.w = Result(self.topic, self.width(), self.height(), self.isMaximized(), mark)
            self.w.show()
            return
        self.spinBoxScore.setValue(0)
        key = self.keys[self.i]
        self.labelQuestion.setText(key)
        self.labelExplanation1.setText(self.dict[key][0])
        self.labelExplanation2.setText(self.dict[key][1])

    def design(self):
        if self.topic == "white":
            style = 'background: rgb(255,255,255);color: rgb(0,0,0);'
            self.ButtonNext.setStyleSheet(style)
            self.spinBoxScore.setStyleSheet(style)
        else:
            style = 'background: rgb(10,10,10);color: rgb(255,255,255); \
                                 border-color: rgb(255,255,255);border-style: solid; \
                                 border-radius: 4px; border-width: 3px;'
            self.spinBoxScore.setStyleSheet(style)
            self.ButtonNext.setStyleSheet(style)
            style = 'color: rgb(255,255,255);'
            self.labelQuestion.setStyleSheet(style)
            self.labelExplanation1.setStyleSheet(style)
            self.labelExplanation2.setStyleSheet(style)
            self.trash.setStyleSheet(style)
