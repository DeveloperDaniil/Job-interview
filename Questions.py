import ctypes
from _csv import writer

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtGui import QPalette, QBrush, QPixmap, QImage, QIcon
from PyQt5.QtWidgets import QMainWindow

from Neuron import processing
from Result import Result

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
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(10)
        Dialog.setFont(font)

        self.TextEdit = QtWidgets.QTextBrowser(Dialog)
        self.TextEdit.setGeometry(QtCore.QRect(10, 10, 1260, 570))
        self.TextEdit.setMinimumSize(QtCore.QSize(0, 2))
        self.TextEdit.setFont(font)
        self.TextEdit.setObjectName("TextEdit")

        font.setPointSize(14)

        self.pushButtonNext = QtWidgets.QPushButton(Dialog)
        self.pushButtonNext.setGeometry(QtCore.QRect(540, 590, 330, 30))
        self.pushButtonNext.setFont(font)
        self.pushButtonNext.setObjectName("pushButtonPred")

        font.setPointSize(16)
        font.setBold(True)

        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(10, 590, 1260, 30))
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")

        self.horizontalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 630, 1260, 80))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.radioLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.radioLayout.setContentsMargins(0, 0, 0, 0)
        self.radioLayout.setObjectName("radioLayout")

        # ////////////////////////////////////////////////////////////////////////////

        font.setPointSize(30)

        self.spinBox = QtWidgets.QSpinBox(Dialog)
        self.spinBox.setGeometry(QtCore.QRect(940, 590, 330, 30))
        self.spinBox.setFont(font)
        self.spinBox.setObjectName("spinBox")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Внимание! Это анонимный опрос. Пожалуйста, отвечайте честно."))
        self.pushButtonNext.setText(_translate("Dialog", "Следующий вопрос"))


class Questions(QMainWindow, Ui_Dialog):
    resized = QtCore.pyqtSignal()

    def __init__(self, topic, x, y, m, name, self1=None):
        super().__init__()
        self.topic = topic
        self.lst_radio = []
        self.data = []
        self.back = False
        self.type = ""
        self.number = 1
        self.self1 = self1
        self.name = name
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

        self.TextEdit.move(int(self.width() * 0.0078125), int(self.height() * 0.013888888888888))
        self.TextEdit.setFixedSize(int(self.width() * 0.984375), int(self.height() * 0.79166666))

        self.label.move(int(self.width() * 0.0078125), int(self.height() * 0.819444444444444444))
        self.label.setFixedSize(int(self.width() * 0.71875), int(self.height() * 0.041666666666))

        self.pushButtonNext.move(int(self.width() * 0.734375), int(self.height() * 0.819444444444444444))
        self.pushButtonNext.setFixedSize(int(self.width() * 0.2578125), int(self.height() * 0.041666666666))

        self.horizontalLayoutWidget.move(int(self.width() * 0.0078125), int(self.height() * 0.875))
        self.horizontalLayoutWidget.setFixedSize(int(self.width() * 0.984375), int(self.height() * 0.1111111111111111))

        self.spinBox.move(int(self.width() * 0.0078125), int(self.height() * 0.875))
        self.spinBox.setFixedSize(int(self.width() * 0.2578125), int(self.height() * 0.1111111111111111))

        return super(Questions, self).resizeEvent(event)

    def radio(self, buttons):
        while self.radioLayout.count():
            child = self.radioLayout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(10)
        self.lst_radio = []
        for i in buttons:
            rd = QtWidgets.QRadioButton("radioButton")
            rd.setText(i)
            rd.setFont(font)
            self.lst_radio.append(rd)
            self.radioLayout.addWidget(rd)

    def change_type(self):
        with open(f"layouts/{self.name}/{self.number}.txt", "r") as file:
            txt = []
            line = file.readline().rstrip()
            while line != "***№№№###buttons***№№№###" and line != "***№№№###range***№№№###":
                txt.append(line)
                line = file.readline().rstrip()
            # self.TextEdit.clear()
            self.TextEdit.setText("\n".join(txt))
            if line == "***№№№###buttons***№№№###":
                self.type = "buttons"
                self.spinBox.setVisible(False)
                self.horizontalLayoutWidget.setVisible(True)
                colRd = int(file.readline().rstrip())
                buttons = []
                for i in range(colRd):
                    buttons.append(file.readline().rstrip())
                self.radio(buttons)
            else:
                self.type = "range"
                self.spinBox.setVisible(True)
                self.horizontalLayoutWidget.setVisible(False)
                self.spinBox.setMinimum(int(file.readline().rstrip()))
                self.spinBox.setMaximum(int(file.readline().rstrip()))
                self.spinBox.setValue(int(file.readline().rstrip()))

    def logic(self):
        self.change_type()
        self.pushButtonNext.clicked.connect(self.next_question)

    def revert(self):
        self.data.append(self.spinBox.value())
        with open(f'layouts/{self.name}/base.csv', 'a', newline='') as file:
            writer_object = writer(file)
            writer_object.writerow(self.data)
        self.self1.setVisible(True)
        self.close()

    def next_question(self):
        if self.back:
            self.revert()
        if self.type == "buttons":
            for i in self.lst_radio:
                if i.isChecked():
                    self.data.append(self.lst_radio.index(i))
                    break
            else:
                ctypes.windll.user32.MessageBoxW(0,
                                                 "Пожалуйста, выберете один из вариантов ответа",
                                                 "Информация", 0)
                return
        else:
            self.data.append(self.spinBox.value())
        self.number += 1  # идем далее(доработать)
        try:
            open(f"layouts/{self.name}/{self.number}.txt", "r")
        except Exception:
            if self.self1:
                self.setWindowTitle(f'Вопрос №{self.number}')
                self.TextEdit.setText("Сколько дней вы уже проработали + сколько еще планируете проработать")
                self.spinBox.setVisible(True)
                self.horizontalLayoutWidget.setVisible(False)
                self.spinBox.setMinimum(0)
                self.spinBox.setMaximum(99999)
                self.spinBox.setValue(0)
                self.back = True
                return
            else:
                mark = processing(self.data, self.name)
                self.w = Result(self.topic, self.width(), self.height(), self.isMaximized(), mark)
                self.w.show()
                self.close()
                return
        self.setWindowTitle(f'Вопрос №{self.number}')
        self.change_type()

    def design(self):
        if self.topic == "white":
            style = 'background: rgb(255,255,255);color: rgb(0,0,0);'
            self.pushButtonNext.setStyleSheet(style)
            self.spinBox.setStyleSheet(style)
            self.TextEdit.setStyleSheet("""
                QTextBrowser {
                    background-color: rgb(255,255,255);
                    border-color: transparent;
                    border-style: solid;
                    border-radius: 4px;
                    border-width: 3px;
                }""" """
                QScrollBar:vertical
                {
                    background-color: transparent;
                    width: 15px;
                    margin: 15px 3px 15px 3px;
                    border: 1px transparent #2A2929;
                    border-radius: 4px;
                }
                QScrollBar::handle:vertical
                {
                    background-color: rgb(120,120,120);
                    min-height: 5px;
                    border-radius: 3px;
                }
                QScrollBar::sub-line:vertical
                {
                    margin: 3px 0px 3px 0px;
                    border-image: url(:/qss_icons/rc/up_arrow_disabled.png);
                    height: 10px;
                    width: 10px;
                    subcontrol-position: top;
                    subcontrol-origin: margin;
                }
                QScrollBar::add-line:vertical
                {
                    margin: 3px 0px 3px 0px;
                    border-image: url(:/qss_icons/rc/down_arrow_disabled.png);
                    height: 10px;
                    width: 10px;
                    subcontrol-position: bottom;
                    subcontrol-origin: margin;
                }
                QScrollBar::sub-line:vertical:hover,QScrollBar::sub-line:vertical:on
                {
                    border-image: url(:/qss_icons/rc/up_arrow.png);
                    height: 10px;
                    width: 10px;
                    subcontrol-position: top;
                    subcontrol-origin: margin;
                }
                QScrollBar::add-line:vertical:hover, QScrollBar::add-line:vertical:on
                {
                    border-image: url(:/qss_icons/rc/down_arrow.png);
                    height: 10px;
                    width: 10px;
                    subcontrol-position: bottom;
                    subcontrol-origin: margin;
                }
                QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical
                {
                    background: none;
                }
                QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical
                {
                    background: none;
                }""")
        else:
            style = 'background: rgb(10,10,10);color: rgb(150,150,150); \
                                 border-color: rgb(50,50,50);border-style: solid; \
                                 border-radius: 4px; border-width: 3px;'
            self.pushButtonNext.setStyleSheet(style)
            self.spinBox.setStyleSheet(style)
            style = 'color: rgb(150,150,150);'
            self.label.setStyleSheet(style)
            self.horizontalLayoutWidget.setStyleSheet("QRadioButton { color: rgb(150,150,150);}")
            self.TextEdit.setStyleSheet("""
                QTextBrowser {
                    background: rgb(10,10,10);color: 
                    rgb(150,150,150);
                    border-color: rgb(50,50,50);border-style: solid;
                    border-radius: 4px; border-width: 3px;}""" """
                QScrollBar:vertical
                {
                    background-color: transparent;
                    width: 15px;
                    margin: 15px 3px 15px 3px;
                    border: 1px transparent #2A2929;
                    border-radius: 4px;
                }
                QScrollBar::handle:vertical
                {
                    background-color: rgb(100,100,100);
                    min-height: 5px;
                    border-radius: 4px;
                }
                QScrollBar::sub-line:vertical
                {
                    margin: 3px 0px 3px 0px;
                    border-image: url(:/qss_icons/rc/up_arrow_disabled.png);
                    height: 10px;
                    width: 10px;
                    subcontrol-position: top;
                    subcontrol-origin: margin;
                }
                QScrollBar::add-line:vertical
                {
                    margin: 3px 0px 3px 0px;
                    border-image: url(:/qss_icons/rc/down_arrow_disabled.png);
                    height: 10px;
                    width: 10px;
                    subcontrol-position: bottom;
                    subcontrol-origin: margin;
                }
                QScrollBar::sub-line:vertical:hover,QScrollBar::sub-line:vertical:on
                {
                    border-image: url(:/qss_icons/rc/up_arrow.png);
                    height: 10px;
                    width: 10px;
                    subcontrol-position: top;
                    subcontrol-origin: margin;
                }
                QScrollBar::add-line:vertical:hover, QScrollBar::add-line:vertical:on
                {
                    border-image: url(:/qss_icons/rc/down_arrow.png);
                    height: 10px;
                    width: 10px;
                    subcontrol-position: bottom;
                    subcontrol-origin: margin;
                }
                QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical
                {
                    background: none;
                }
                QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical
                {
                    background: none;
                }""")
