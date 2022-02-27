import ctypes
import shutil

from PyQt5 import QtCore, QtWidgets, QtGui, Qt
from PyQt5.QtCore import pyqtSlot, QTimer, pyqtSignal
from PyQt5.QtGui import QPalette, QBrush, QPixmap, QImage, QIcon
from PyQt5.QtWidgets import QMainWindow, QInputDialog

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
        self.comboBox = QtWidgets.QComboBox(Dialog)
        self.comboBox.setGeometry(QtCore.QRect(10, 590, 220, 30))
        self.comboBox.setFont(font)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.TextEdit = QtWidgets.QPlainTextEdit(Dialog)
        self.TextEdit.setGeometry(QtCore.QRect(10, 10, 1260, 570))
        self.TextEdit.setMinimumSize(QtCore.QSize(0, 2))
        self.TextEdit.setFont(font)
        self.TextEdit.setObjectName("TextEdit")
        self.horizontalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 630, 1260, 80))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.radioLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.radioLayout.setContentsMargins(0, 0, 0, 0)
        self.radioLayout.setObjectName("radioLayout")
        self.labelCol = QtWidgets.QLabel(Dialog)
        self.labelCol.setGeometry(QtCore.QRect(240, 590, 100, 30))
        self.labelCol.setFont(font)
        self.labelCol.setObjectName("label")
        self.spinBoxRad = QtWidgets.QSpinBox(Dialog)
        self.spinBoxRad.setGeometry(QtCore.QRect(350, 590, 100, 30))
        self.spinBoxRad.setFont(font)
        self.spinBoxRad.setMinimum(2)
        self.spinBoxRad.setMaximum(10)
        self.spinBoxRad.setObjectName("spinBox")
        self.pushButtonPred = QtWidgets.QPushButton(Dialog)
        self.pushButtonPred.setGeometry(QtCore.QRect(510, 590, 200, 30))
        self.pushButtonPred.setFont(font)
        self.pushButtonPred.setObjectName("pushButtonPred")
        self.pushButtonNext = QtWidgets.QPushButton(Dialog)
        self.pushButtonNext.setGeometry(QtCore.QRect(720, 590, 200, 30))
        self.pushButtonNext.setFont(font)
        self.pushButtonNext.setObjectName("pushButtonNext")
        self.pushButtonSave = QtWidgets.QPushButton(Dialog)
        self.pushButtonSave.setGeometry(QtCore.QRect(940, 590, 160, 30))
        self.pushButtonSave.setFont(font)
        self.pushButtonSave.setObjectName("pushButtonSave")
        self.pushButtonCancle = QtWidgets.QPushButton(Dialog)
        self.pushButtonCancle.setGeometry(QtCore.QRect(1110, 590, 160, 30))
        self.pushButtonCancle.setFont(font)
        self.pushButtonCancle.setObjectName("pushButtonCancle")

        self.labelOt = QtWidgets.QLabel(Dialog)
        self.labelOt.setGeometry(QtCore.QRect(240, 590, 31, 30))
        self.labelOt.setFont(font)
        self.labelOt.setObjectName("labelOt")
        self.labelOt.setVisible(False)
        self.spinBoxOt = QtWidgets.QSpinBox(Dialog)
        self.spinBoxOt.setGeometry(QtCore.QRect(280, 590, 60, 30))
        self.spinBoxOt.setFont(font)
        self.spinBoxOt.setMinimum(-999999)
        self.spinBoxOt.setMaximum(999999)
        self.spinBoxOt.setProperty("value", 0)
        self.spinBoxOt.setObjectName("spinBoxOt")
        self.spinBoxOt.setVisible(False)
        self.spinBoxDo = QtWidgets.QSpinBox(Dialog)
        self.spinBoxDo.setGeometry(QtCore.QRect(390, 590, 60, 30))
        self.spinBoxDo.setFont(font)
        self.spinBoxDo.setMinimum(-999999)
        self.spinBoxDo.setMaximum(999999)
        self.spinBoxDo.setProperty("value", 10)
        self.spinBoxDo.setObjectName("spinBoxDo")
        self.spinBoxDo.setVisible(False)
        self.labelDo = QtWidgets.QLabel(Dialog)
        self.labelDo.setGeometry(QtCore.QRect(350, 590, 31, 30))
        self.labelDo.setFont(font)
        self.labelDo.setObjectName("labelDo")
        self.labelDo.setVisible(False)
        self.spinBox = QtWidgets.QSpinBox(Dialog)
        self.spinBox.setGeometry(QtCore.QRect(45, 630, 150, 50))
        self.spinBox.setFont(font)
        self.spinBox.setObjectName("spinBox")
        self.spinBox.setMinimum(0)
        self.spinBox.setMaximum(10)
        self.spinBox.setVisible(False)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.comboBox.setItemText(0, _translate("Dialog", "Макет с кнопками"))
        self.comboBox.setItemText(1, _translate("Dialog", "Макет с диапазоном"))
        self.labelCol.setText(_translate("Dialog", "Количество:"))
        self.pushButtonPred.setText(_translate("Dialog", "<Предыдущий вопрос"))
        self.pushButtonNext.setText(_translate("Dialog", "Следующий вопрос>"))
        self.pushButtonCancle.setText(_translate("Dialog", "Отмена"))
        self.pushButtonSave.setText(_translate("Dialog", "Сохранить макет"))
        self.labelOt.setText(_translate("Dialog", "От:"))
        self.labelDo.setText(_translate("Dialog", "До:"))


class QDoubleRadioButton(Qt.QRadioButton):
    doubleClicked = pyqtSignal()
    clicked = pyqtSignal()

    def __init__(self, *args, **kwargs):
        Qt.QRadioButton.__init__(self, *args, **kwargs)
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.clicked.emit)
        super().clicked.connect(self.check_double_click)

    @pyqtSlot()
    def check_double_click(self):
        if self.timer.isActive():
            self.doubleClicked.emit()
            self.timer.stop()
        else:
            self.timer.start(250)


class Editor(QMainWindow, Ui_Dialog):
    resized = QtCore.pyqtSignal()

    def __init__(self, topic, x, y, m, self1, name, number, delete=True):
        super().__init__()
        self.self1 = self1
        self.topic = topic
        self.number = number
        self.delete = delete
        self.lst_radio = []
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
        self.fill_layout()
        self.logic()

    def closeEvent(self, event):
        if self.delete:
            shutil.rmtree(f'layouts/{self.name}')
        self.self1.fill_in_the_table()
        self.self1.setVisible(True)

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

        self.comboBox.move(int(self.width() * 0.0078125), int(self.height() * 0.819444444444444))
        self.comboBox.setFixedSize(int(self.width() * 0.171875), int(self.height() * 0.04166666))

        self.labelCol.move(int(self.width() * 0.1875), int(self.height() * 0.819444444444444))
        self.labelCol.setFixedSize(int(self.width() * 0.078125), int(self.height() * 0.04166666))

        self.spinBoxRad.move(int(self.width() * 0.2734375), int(self.height() * 0.819444444444444))
        self.spinBoxRad.setFixedSize(int(self.width() * 0.078125), int(self.height() * 0.04166666))

        self.horizontalLayoutWidget.move(int(self.width() * 0.0078125), int(self.height() * 0.875))
        self.horizontalLayoutWidget.setFixedSize(int(self.width() * 0.984375), int(self.height() * 0.1111111111111111))

        self.pushButtonPred.move(int(self.width() * 0.3984375), int(self.height() * 0.819444444444444))
        self.pushButtonPred.setFixedSize(int(self.width() * 0.15625), int(self.height() * 0.04166666))

        self.pushButtonNext.move(int(self.width() * 0.5625), int(self.height() * 0.819444444444444))
        self.pushButtonNext.setFixedSize(int(self.width() * 0.15625), int(self.height() * 0.04166666))

        self.pushButtonSave.move(int(self.width() * 0.734375), int(self.height() * 0.819444444444444))
        self.pushButtonSave.setFixedSize(int(self.width() * 0.125), int(self.height() * 0.04166666))

        self.pushButtonCancle.move(int(self.width() * 0.8671875), int(self.height() * 0.819444444444444))
        self.pushButtonCancle.setFixedSize(int(self.width() * 0.125), int(self.height() * 0.04166666))

        self.spinBox.move(int(self.width() * 0.03515625), int(self.height() * 0.89583333333333333333333333333))
        self.spinBox.setFixedSize(int(self.width() * 0.1171875), int(self.height() * 0.0694444444444444444444))

        self.spinBoxOt.move(int(self.width() * 0.21875), int(self.height() * 0.819444444444444))
        self.spinBoxOt.setFixedSize(int(self.width() * 0.046875), int(self.height() * 0.04166666))

        self.spinBoxDo.move(int(self.width() * 0.304675), int(self.height() * 0.819444444444444))
        self.spinBoxDo.setFixedSize(int(self.width() * 0.046875), int(self.height() * 0.04166666))

        self.labelDo.move(int(self.width() * 0.2734375), int(self.height() * 0.819444444444444))
        self.labelDo.setFixedSize(int(self.width() * 0.0234375), int(self.height() * 0.04166666))

        self.labelOt.move(int(self.width() * 0.1875), int(self.height() * 0.819444444444444))
        self.labelOt.setFixedSize(int(self.width() * 0.0234375), int(self.height() * 0.04166666))

        return super(Editor, self).resizeEvent(event)

    def write(self):
        with open(f"layouts/{self.name}/{self.number}.txt", "w+") as file:
            file.write(self.TextEdit.toPlainText())
            file.write("\n")
            if self.comboBox.currentText() == "Макет с кнопками":
                file.write("***№№№###buttons***№№№###")
                file.write("\n")
                file.write(f"{self.spinBoxRad.value()}")
                file.write("\n")
                for i in self.lst_radio:
                    file.write(i.text())
                    file.write("\n")
            else:
                file.write("***№№№###range***№№№###")
                file.write("\n")
                file.write(f"{self.spinBoxOt.value()}")
                file.write("\n")
                file.write(f"{self.spinBoxDo.value()}")
                file.write("\n")
                file.write(f"{self.spinBox.value()}")
                file.write("\n")

    def fill_layout(self):
        try:
            with open(f"layouts/{self.name}/{self.number}.txt", "r") as file:
                txt = []
                line = file.readline().rstrip()
                while line != "***№№№###buttons***№№№###" and line != "***№№№###range***№№№###":
                    txt.append(line)
                    line = file.readline().rstrip()
                self.TextEdit.clear()
                self.TextEdit.appendPlainText("\n".join(txt))
                if line == "***№№№###buttons***№№№###":
                    self.comboBox.setCurrentIndex(0)
                    line = file.readline().rstrip()
                    self.spinBoxRad.setValue(int(line))
                    self.radio()
                    for i in self.lst_radio:
                        line = file.readline().rstrip()
                        i.setText(line)
                    self.spinBoxOt.setValue(0)
                    self.spinBoxDo.setValue(10)
                    self.spinBox.setMinimum(0)
                    self.spinBox.setMaximum(10)
                    self.spinBox.setValue(0)
                else:
                    self.comboBox.setCurrentIndex(1)
                    line = file.readline().rstrip()
                    self.spinBoxOt.setValue(int(line))
                    self.spinBox.setMinimum(int(line))
                    line = file.readline().rstrip()
                    self.spinBoxDo.setValue(int(line))
                    self.spinBox.setMaximum(int(line))
                    line = file.readline().rstrip()
                    self.spinBox.setValue(int(line))
        except Exception:
            self.comboBox.setCurrentIndex(0)
            self.TextEdit.clear()
            self.spinBoxRad.setValue(2)
            for i in self.lst_radio:
                i.setParent(None)
            self.lst_radio = []
            self.spinBoxOt.setValue(0)
            self.spinBoxDo.setValue(10)
            self.spinBox.setMinimum(0)
            self.spinBox.setMaximum(10)
            self.spinBox.setValue(0)
            self.radio()

    def change_number(self):
        if self.number == 1 and self.sender().objectName() == "pushButtonPred":
            ctypes.windll.user32.MessageBoxW(0, "Вы находитесь на первом вопросе", "Ошибка", 0)
            return
        if self.TextEdit.toPlainText() == "" and self.sender().objectName() != "pushButtonPred":
            ctypes.windll.user32.MessageBoxW(0, "Вы не заполнили поле вопроса", "Ошибка", 0)
            return
        if self.TextEdit.toPlainText():
            self.write()
        if self.sender().objectName() == "pushButtonNext":
            self.number += 1
        else:
            self.number -= 1
        self.setWindowTitle(f'Вопрос №{self.number}')
        self.fill_layout()

    def radio(self):
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(10)
        if self.spinBoxRad.value() < len(self.lst_radio):
            while self.spinBoxRad.value() < len(self.lst_radio):
                self.lst_radio[-1].setParent(None)
                del self.lst_radio[-1]
            return
        for i in range(self.spinBoxRad.value() - len(self.lst_radio)):
            rd = QDoubleRadioButton("radioButton")
            rd.doubleClicked.connect(self.change_radio_text)
            rd.setFont(font)
            self.lst_radio.append(rd)
            self.radioLayout.addWidget(rd)

    def close_win(self):
        self.close()

    def change_radio_text(self):
        name, ok_pressed = QInputDialog.getText(self, "Изменить текст кнопки",
                                                "Введите текст кнопки")
        if not ok_pressed:
            return
        self.sender().setText(name)

    def change_type(self):
        if self.comboBox.currentText() == "Макет с кнопками":
            self.spinBox.setVisible(False)
            self.labelOt.setVisible(False)
            self.spinBoxOt.setVisible(False)
            self.spinBoxDo.setVisible(False)
            self.labelDo.setVisible(False)

            self.horizontalLayoutWidget.setVisible(True)
            self.labelCol.setVisible(True)
            self.spinBoxRad.setVisible(True)
        else:
            self.spinBox.setVisible(True)
            self.labelOt.setVisible(True)
            self.spinBoxOt.setVisible(True)
            self.spinBoxDo.setVisible(True)
            self.labelDo.setVisible(True)

            self.horizontalLayoutWidget.setVisible(False)
            self.labelCol.setVisible(False)
            self.spinBoxRad.setVisible(False)

    def change_range(self):
        if self.sender().objectName() == "spinBoxOt":
            if self.spinBoxDo.value() == self.spinBoxOt.value():
                self.spinBoxDo.setValue(self.spinBoxDo.value() + 1)
        else:
            if self.spinBoxOt.value() == self.spinBoxDo.value():
                self.spinBoxOt.setValue(self.spinBoxOt.value() - 1)
        self.spinBox.setMinimum(self.spinBoxOt.value())
        self.spinBox.setMaximum(self.spinBoxDo.value())

    def save_layout(self):
        if self.TextEdit.toPlainText():
            self.write()
        self.delete = False
        self.close()

    def logic(self):

        self.spinBoxRad.valueChanged.connect(self.radio)
        self.comboBox.currentTextChanged.connect(self.change_type)
        self.spinBoxOt.valueChanged.connect(self.change_range)
        self.spinBoxDo.valueChanged.connect(self.change_range)
        self.pushButtonCancle.clicked.connect(self.close_win)
        self.pushButtonNext.clicked.connect(self.change_number)
        self.pushButtonPred.clicked.connect(self.change_number)
        self.pushButtonSave.clicked.connect(self.save_layout)

    def design(self):
        if self.topic == "white":
            style = 'background: rgb(255,255,255);color: rgb(0,0,0);'
            self.comboBox.setStyleSheet(style)
            self.spinBoxRad.setStyleSheet(style)
            self.pushButtonPred.setStyleSheet(style)
            self.pushButtonNext.setStyleSheet(style)
            self.pushButtonCancle.setStyleSheet(style)
            self.pushButtonSave.setStyleSheet(style)
            self.spinBox.setStyleSheet(style)
            self.spinBoxOt.setStyleSheet(style)
            self.spinBoxDo.setStyleSheet(style)
            self.TextEdit.setStyleSheet("""
                QPlainTextEdit {
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
            self.pushButtonPred.setStyleSheet(style)
            self.pushButtonNext.setStyleSheet(style)
            self.pushButtonCancle.setStyleSheet(style)
            self.pushButtonSave.setStyleSheet(style)
            self.comboBox.setStyleSheet(style)
            self.spinBoxRad.setStyleSheet(style)
            self.spinBox.setStyleSheet(style)
            self.spinBoxOt.setStyleSheet(style)
            self.spinBoxDo.setStyleSheet(style)
            style = 'color: rgb(150,150,150);'
            self.labelCol.setStyleSheet(style)
            self.labelDo.setStyleSheet(style)
            self.labelOt.setStyleSheet(style)
            self.horizontalLayoutWidget.setStyleSheet("QRadioButton { color: rgb(150,150,150);}")
            self.TextEdit.setStyleSheet("""
                QPlainTextEdit {
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
