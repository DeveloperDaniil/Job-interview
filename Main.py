import ctypes
import os
import shutil
import subprocess
import sys
import zipfile

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPalette, QBrush, QPixmap, QImage, QFont, QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication, QInputDialog, QFileDialog

from Authors import Authors
from Layouts import Layouts

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
        self.ButtonReColour = QtWidgets.QPushButton(Dialog)
        self.ButtonReColour.setGeometry(QtCore.QRect(0, 0, 31, 28))
        self.ButtonReColour.setText("")
        if topic == "white":
            self.ButtonReColour.setIcon(QtGui.QIcon('images/re_colour_white.png'))
        else:
            self.ButtonReColour.setIcon(QtGui.QIcon('images/re_colour_black.png'))
        self.ButtonReColour.setObjectName("ButtonReColour")
        self.ButtonReColour.setStyleSheet('background: rgba(255,255,255,0);')
        self.ButtonStart = QtWidgets.QPushButton(Dialog)
        self.ButtonStart.setGeometry(QtCore.QRect(300, 260, 551, 71))
        self.ButtonStart.setObjectName("ButtonStart")
        self.ButtonStart.setFont(QFont('Century Gothic', 13))
        self.ButtonAftors = QtWidgets.QPushButton(Dialog)
        self.ButtonAftors.setGeometry(QtCore.QRect(300, 340, 551, 71))
        self.ButtonAftors.setObjectName("ButtonAftors")
        self.ButtonAftors.setFont(QFont('Century Gothic', 13))
        self.ImportExport = QtWidgets.QPushButton(Dialog)
        self.ImportExport.setGeometry(QtCore.QRect(300, 420, 551, 71))
        self.ImportExport.setObjectName("AboutProgram")
        self.ImportExport.setFont(QFont('Century Gothic', 13))
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.ButtonStart.setText(_translate("Dialog", "Выбрать макет"))
        self.ButtonAftors.setText(_translate("Dialog", "Авторы"))
        self.ImportExport.setText(_translate("Dialog", "Импорт/Экспорт"))


class Main(QMainWindow, Ui_Dialog):
    resized = QtCore.pyqtSignal()

    def __init__(self, topic="white", x=1280, y=720, m=False):
        super().__init__()
        self.topic = topic
        if topic == "white":
            self.im = QImage()
            self.im.load("images/white_background.jpg")
        else:
            self.im = QImage()
            self.im.load("images/black_background.jpg")
        self.setupUi(self, topic)
        self.setWindowTitle('Собеседование')
        self.design()
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
            return
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap(QPixmap.fromImage(self.im))))
        self.setPalette(palette)

    def resizeEvent(self, event):
        self.resized.emit()
        self.resize_image()

        self.ButtonStart.move(int(self.width() * 0.286), int(self.height() * 0.36))
        self.ButtonStart.setFixedSize(int(self.width() * 0.4276), int(self.height() * 0.095))

        self.ButtonAftors.move(int(self.width() * 0.286), int(self.height() * 0.46))
        self.ButtonAftors.setFixedSize(int(self.width() * 0.4276), int(self.height() * 0.095))

        self.ImportExport.move(int(self.width() * 0.286), int(self.height() * 0.56))
        self.ImportExport.setFixedSize(int(self.width() * 0.4276), int(self.height() * 0.095))

        return super(Main, self).resizeEvent(event)

    def logic(self):
        self.ButtonReColour.clicked.connect(self.re_color)
        self.ButtonStart.clicked.connect(self.new_win)
        self.ButtonAftors.clicked.connect(self.autors)
        self.ImportExport.clicked.connect(self.import_export)

    def import_export(self):
        action, ok_pressed = QInputDialog.getItem(
            self, "Импорт/экспорт", "Выберите действие",
            ("Экспортировать макеты на рабочий стол", "Импортировать макеты"), 0, False)
        if not ok_pressed:
            return
        if action == "Экспортировать макеты на рабочий стол":
            shutil.make_archive("layouts", 'zip', "layouts")
            output = subprocess.check_output(r'powershell -command "[Environment]::GetFolderPath(\"Desktop\")"')
            path = output.decode().strip()
            try:
                os.rename('layouts.zip', f'{path}/layouts.zip')
            except Exception:
                os.remove(f'{path}/layouts.zip')
                os.rename('layouts.zip', f'{path}\layouts.zip')
        else:
            message = f'Вы уверены? Макеты, которые у вас есть сейчас, заменятся новыми'
            reply = QtWidgets.QMessageBox.question(self, 'Уведомление', message,
                                                   QtWidgets.QMessageBox.Yes,
                                                   QtWidgets.QMessageBox.No)
            if reply == QtWidgets.QMessageBox.No:
                return
            desc = subprocess.check_output(r'powershell -command "[Environment]::GetFolderPath(\"Desktop\")"')
            desc = desc.decode("utf-8").rstrip()
            file_name = QFileDialog.getOpenFileName(
                self, 'Выбрать архив с макетами', desc,
                'Архив (*.zip);')[0]
            shutil.rmtree('layouts')
            os.mkdir('layouts')
            with zipfile.ZipFile(file_name, 'r') as zip_file:
                zip_file.extractall('layouts')

    def autors(self):
        self.close()
        self.w = Authors(self.topic, self.width(), self.height(), self.isMaximized())
        self.w.show()

    def new_win(self):
        self.close()
        self.w = Layouts(self.topic, self.width(), self.height(), self.isMaximized())
        self.w.show()

    def re_color(self):
        if self.topic == "white":
            self.topic = "black"
            self.im.load("images/black_background.jpg")
            style = 'background: rgb(10,10,10);color: rgb(150,150,150); \
                     border-color: rgb(50,50,50);border-style: solid; \
                     border-radius: 4px; border-width: 3px;'
            self.ButtonReColour.setIcon(QtGui.QIcon('images/re_colour_black.png'))
        else:
            self.topic = "white"
            self.im.load("images/white_background.jpg")
            style = 'background: rgb(255,255,255);color: rgb(0,0,0);'
            self.ButtonReColour.setIcon(QtGui.QIcon('images/re_colour_white.png'))
        self.ButtonStart.setStyleSheet(style)
        self.ButtonAftors.setStyleSheet(style)
        self.ImportExport.setStyleSheet(style)
        self.resize_image()

    def design(self):
        if self.topic == "white":
            style = 'background: rgb(255,255,255);color: rgb(0,0,0);'
            self.ButtonStart.setStyleSheet(style)
            self.ButtonAftors.setStyleSheet(style)
            self.ImportExport.setStyleSheet(style)
        else:
            style = 'background: rgb(10,10,10);color: rgb(150,150,150); \
                                 border-color: rgb(50,50,50);border-style: solid; \
                                 border-radius: 4px; border-width: 3px;'
            self.ButtonStart.setStyleSheet(style)
            self.ButtonAftors.setStyleSheet(style)
            self.ImportExport.setStyleSheet(style)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    ex.show()
    sys.exit(app.exec())
