import ctypes
import glob
import os
import shutil

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.Qt import QPushButton
from PyQt5.QtGui import QPalette, QBrush, QPixmap, QImage, QIcon
from PyQt5.QtWidgets import QMainWindow, QHeaderView, QInputDialog

from Editor import Editor
from Questions import Questions

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
        font.setPointSize(14)
        self.tableWidget = QtWidgets.QTableWidget(Dialog)
        self.tableWidget.setGeometry(QtCore.QRect(10, 10, 1260, 620))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(1)
        self.tableWidget.setRowCount(0)
        self.tableWidget.horizontalHeader().hide()
        self.tableWidget.verticalHeader().hide()
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.setFont(font)
        self.tableWidget.setSelectionMode(self.tableWidget.NoSelection)
        font.setPointSize(11)
        self.pushButtonStart = QtWidgets.QPushButton(Dialog)
        self.pushButtonStart.setGeometry(QtCore.QRect(11, 640, 307, 70))
        self.pushButtonStart.setFont(font)
        self.pushButtonStart.setObjectName("pushButtonStart")
        font.setPointSize(14)
        self.pushButtonTransform = QtWidgets.QPushButton(Dialog)
        self.pushButtonTransform.setGeometry(QtCore.QRect(328, 640, 307, 70))
        self.pushButtonTransform.setFont(font)
        self.pushButtonTransform.setObjectName("pushButtonTransform")
        self.pushButtonAdd = QtWidgets.QPushButton(Dialog)
        self.pushButtonAdd.setGeometry(QtCore.QRect(645, 640, 307, 70))
        self.pushButtonAdd.setFont(font)
        self.pushButtonAdd.setObjectName("pushButtonAdd")
        self.pushButtonDell = QtWidgets.QPushButton(Dialog)
        self.pushButtonDell.setGeometry(QtCore.QRect(962, 640, 307, 70))
        self.pushButtonDell.setFont(font)
        self.pushButtonDell.setObjectName("pushButtonDell")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButtonStart.setText(_translate("Dialog", "Начать работу с этим макетом"))
        self.pushButtonTransform.setText(_translate("Dialog", "Изменить макет"))
        self.pushButtonDell.setText(_translate("Dialog", "Удалить макет"))
        self.pushButtonAdd.setText(_translate("Dialog", "Добавить макет"))


class Layouts(QMainWindow, Ui_Dialog):
    resized = QtCore.pyqtSignal()

    def __init__(self, topic, x, y, m):
        super().__init__()
        self.selectedButton = ""
        self.buttons = []
        self.topic = topic
        if topic == "white":
            self.im = QImage()
            self.im.load("images/white_background.jpg")
        else:
            self.im = QImage()
            self.im.load("images/black_background.jpg")
        self.setupUi(self, topic)
        self.design()
        self.fill_in_the_table()
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

        self.tableWidget.move(int(self.width() * 0.0078125), int(self.height() * 0.013888888888888))
        self.tableWidget.setFixedSize(int(self.width() * 0.984375), int(self.height() * 0.86111111))

        self.pushButtonStart.move(int(self.width() * 0.00859375), int(self.height() * 0.888888888888))
        self.pushButtonStart.setFixedSize(int(self.width() * 0.23984375), int(self.height() * 0.0972222))

        self.pushButtonTransform.move(int(self.width() * 0.25625), int(self.height() * 0.888888888888))
        self.pushButtonTransform.setFixedSize(int(self.width() * 0.23984375), int(self.height() * 0.0972222))

        self.pushButtonAdd.move(int(self.width() * 0.50390625), int(self.height() * 0.888888888888))
        self.pushButtonAdd.setFixedSize(int(self.width() * 0.23984375), int(self.height() * 0.0972222))

        self.pushButtonDell.move(int(self.width() * 0.7515625), int(self.height() * 0.888888888888))
        self.pushButtonDell.setFixedSize(int(self.width() * 0.23984375), int(self.height() * 0.0972222))

        return super(Layouts, self).resizeEvent(event)

    def fill_in_the_table(self):
        self.buttons = []
        layouts = glob.glob("layouts/*")
        self.tableWidget.setRowCount(len(layouts))
        for col, i in enumerate(layouts):
            btn = QPushButton(i.split("\\")[1])
            btn.clicked.connect(self.choose_button)
            self.buttons.append(btn)
            self.tableWidget.setCellWidget(col, 0, btn)
        self.choose_button()

    def logic(self):
        self.pushButtonDell.clicked.connect(self.dell_layout)
        self.pushButtonAdd.clicked.connect(self.add_layout)
        self.pushButtonTransform.clicked.connect(self.change_layout)
        self.pushButtonStart.clicked.connect(self.start_layout)

    def choose_button(self):
        name = self.sender().text()
        if name == "Выбрать макет":
            name = ""
        self.selectedButton = name
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(14)
        if self.topic == "white":
            # for i in self.buttons:
            #    if i.text() == name:
            #        i.setStyleSheet('background: rgb(190, 190, 190);color: rgb(0,0,0); \
            #                                                 border-color: rgba(0,0,0,0.5);border-style: solid; \
            #                                                 border-radius: 1px; border-width: 1px;')
            #    else:
            #        i.setStyleSheet('color: rgb(0,0,0); \
            #                             border-color: rgba(0,0,0,0.5);border-style: solid; \
            #                             border-radius: 1px; border-width: 1px;')
            #    i.setFont(font)
            for i in self.buttons:
                if i.text() == name:
                    i.setStyleSheet("""
                    QPushButton {
                        background: rgb(175, 175, 177);
                        color: rgb(0,0,0);
                        border-color: rgba(0,0,0,0.5);
                        border-style: solid;
                        border-radius: 1px;
                        border-width: 1px;
                    }
                    """ "QPushButton:pressed { background-color: rgb(187,187,189) }")
                else:
                    i.setStyleSheet("""
                    QPushButton {
                        color: rgb(0,0,0);
                        border-color: rgba(0,0,0,0.5);
                        border-style: solid;
                        border-radius: 1px;
                        border-width: 1px;
                    }
                    """ "QPushButton:pressed { background-color: rgb(208,208,208) }")
                i.setFont(font)
        else:
            for i in self.buttons:
                if i.text() == name:
                    i.setStyleSheet("""
                    QPushButton {
                        background-color: rgb(41,41,41);
                        color: rgb(150,150,150);
                        border-style: solid;
                        border-radius: 4px;
                        border-width: 3px;
                        border-color: rgb(50,50,50);
                    }
                    """ "QPushButton:pressed { background-color: rgb(35,40,43) }")
                else:
                    i.setStyleSheet("""
                    QPushButton {
                        background: transparent;
                        color: rgb(150,150,150);
                        border-style: solid;
                        border-radius: 4px;
                        border-width: 3px;
                        border-color: rgb(50,50,50);
                    }
                    """ "QPushButton:pressed { background-color: rgb(35,40,43) }")
                i.setFont(font)

    def dell_layout(self):
        if self.selectedButton == "":
            return
        if self.selectedButton == "Стандартный макет":
            ctypes.windll.user32.MessageBoxW(0, "Вы не можете удалить стандартный макет", "Ошибка", 0)
            return
        message = f'Вы уверены, что хотите удалить "{self.selectedButton}"?'
        reply = QtWidgets.QMessageBox.question(self, 'Уведомление', message,
                                               QtWidgets.QMessageBox.Yes,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.No:
            return
        shutil.rmtree(f'layouts/{self.selectedButton}')
        self.selectedButton = ""
        self.fill_in_the_table()

    def add_layout(self):
        name, ok_pressed = QInputDialog.getText(self, "Название шалона",
                                                "Как будет называться макет")
        if not ok_pressed:
            return
        while name in [i.text() for i in self.buttons] or not name:
            ctypes.windll.user32.MessageBoxW(0, "Ошибка", "Такой макет уже существует или вы не ввели название", 0)
            name, ok_pressed = QInputDialog.getText(self, "Название макета",
                                                    "Как будет называться макет")
            if not ok_pressed:
                return
        self.setVisible(False)
        os.mkdir(f'layouts/{name}')
        self.w = Editor(self.topic, self.width(), self.height(), self.isMaximized(), self, name, 1)
        self.w.show()

    def change_layout(self):
        if self.selectedButton == "":
            return
        action, ok_pressed = QInputDialog.getItem(
            self, "Изменение макета", "Выберите действие",
            ("Изменить вопросы макета", "Обучить макет"), 0, False)
        if not ok_pressed:
            return
        if self.selectedButton == "Стандартный макет" and action == "Изменить вопросы макета":
            ctypes.windll.user32.MessageBoxW(0, "Вы не можете изменить вопросы стандартного макета", "Ошибка", 0)
            return
        if action == "Изменить вопросы макета":
            self.setVisible(False)
            self.w = Editor(self.topic, self.width(), self.height(), self.isMaximized(), self, self.selectedButton, 1,
                            False)
            self.w.show()
        else:
            self.setVisible(False)
            self.w = Questions(self.topic, self.width(), self.height(), self.isMaximized(), self.selectedButton, self)
            self.w.show()

    def start_layout(self):
        if self.selectedButton == "":
            return
        try:
            open(f"layouts/{self.selectedButton}/base.csv", "r")
        except Exception:
            ctypes.windll.user32.MessageBoxW(0,
                                             "Этот макет не обучен.\
Для его использования вы должны обучить его во вкладке \"Изменить\".",
                                             "Ошибка", 0)
            return
        self.setVisible(False)
        self.w = Questions(self.topic, self.width(), self.height(), self.isMaximized(), self.selectedButton)
        self.w.show()

    def design(self):
        if self.topic == "white":
            style = 'background: rgb(255,255,255);color: rgb(0,0,0);'
            self.pushButtonAdd.setStyleSheet(style)
            self.pushButtonDell.setStyleSheet(style)
            self.pushButtonTransform.setStyleSheet(style)
            self.pushButtonStart.setStyleSheet(style)
            self.tableWidget.setStyleSheet("""
                            QTableWidget {
                                background-color: transparent;
                                border : None;
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
            self.pushButtonAdd.setStyleSheet(style)
            self.pushButtonDell.setStyleSheet(style)
            self.pushButtonTransform.setStyleSheet(style)
            self.pushButtonStart.setStyleSheet(style)
            self.tableWidget.setStyleSheet("""
                QTableWidget {
                    background-color: transparent;
                    border : None;
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
                    background-color: rgb(100,100,100);
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
