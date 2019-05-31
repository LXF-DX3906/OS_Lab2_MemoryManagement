from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(600, 700)
        MainWindow.setStyleSheet("background-color: rgb(250, 250, 250);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # 添加菜单——模式按钮：可选首次适应算法或最佳适应算法
        self.menu_bar = QMainWindow.menuBar(MainWindow)
        self.model_bar = self.menu_bar.addMenu("Algorithm")
        self.menu_bar.setFont(QtGui.QFont('Microsoft YaHei', 9))
        self.menu_bar.setStyleSheet(
            "QMenuBar::item { \
                color: rgb(255,255,255);  /*字体颜色*/ \
                border: 2px solid rgb(120,120,120); \
                background-color:rgb(124,179,66);\
            } \
            QMenuBar::item:selected { \
                border: 2px solid rgb(66,66,66); \
                background-color:rgb(51,105,30);/*选中的样式*/ \
            } \
            QMenuBar::item:pressed {/*菜单项按下效果*/ \
                border: 2px solid rgb(66,66,66); \
                background-color: rgb(51,105,30); \
            }")

        # 向QMenu小控件中添加按钮，子菜单
        #首次适应算法按钮
        self.firstFit_bar = QtWidgets.QWidgetAction(MainWindow, checkable=True)
        self.firstFit_bar.setChecked(True)
        self.firstFit_action = QtWidgets.QLabel(" √  First fit  ")
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        self.firstFit_action.setFont(font)
        self.firstFit_action.setStyleSheet(
            "QLabel { color: rgb(255,255,255);  /*字体颜色*/ \
                background-color:rgb(51,105,30);\
                }"
            "QLabel:hover{  background-color:rgb(51,105,30);/*选中的样式*/ \
                }"
        )
        self.firstFit_bar.setDefaultWidget(self.firstFit_action)

        #最佳适应算法按钮
        self.bestFit_bar = QtWidgets.QWidgetAction(MainWindow, checkable=True)
        self.bestFit_bar.setChecked(False)
        self.bestFit_action = QtWidgets.QLabel("     Best fit  ")
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        self.bestFit_action.setFont(font)
        self.bestFit_action.setStyleSheet(
            "QLabel { color: rgb(225,225,225);  /*字体颜色*/ \
                background-color:rgb(124,179,66);\
                }"
            "QLabel:hover{ background-color:rgb(51,105,30);/*选中的样式*/ \
                            }"
        )
        self.bestFit_bar.setDefaultWidget(self.bestFit_action)
        #将两按钮添加到model_bar中去
        self.model_bar.addAction(self.firstFit_bar)
        self.model_bar.addAction(self.bestFit_bar)

        # 加入作业lable
        self.lable = QtWidgets.QLabel(MainWindow)
        self.lable.setText("Add Progress")
        self.lable.setGeometry(QtCore.QRect(35, 50, 200, 40))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(15)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.lable.setFont(font)
        self.lable.setStyleSheet("color: rgb(51,105,30);")
        self.lable.setTextFormat(QtCore.Qt.AutoText)
        self.lable.setWordWrap(True)

        # 创建快捷加入按钮
        self.btnGroup = {}
        for i in range(0, 64):
            self.btnGroup[i] = QtWidgets.QPushButton(MainWindow)  # 创建一个按钮，并将按钮加入到窗口MainWindow中
            self.btnGroup[i].setFont(QtGui.QFont('Microsoft YaHei', 6))
            self.btnGroup[i].setText(str(i+1)+'0k')
            self.btnGroup[i].setGeometry(QtCore.QRect(((i//16)+1)*35, 100 + (i % 16) * 31, 30, 30))
            self.btnGroup[i].setStyleSheet("QPushButton{color:rgb(255,255,255)}"
                                           "QPushButton{background-color:rgb(124,179,66)}"
                                           "QPushButton{border: 2px solid rgb(100,100,100)}"
                                           "QPushButton:hover{background-color:rgb(104,159,56)}"
                                           "QPushButton:pressed{background-color:rgb(51,105,30)}")

        # 创建一个文本框，并将按钮加入到窗口MainWindow中
        self.textbox = QtWidgets.QLineEdit(MainWindow)
        self.textbox.setFont(QtGui.QFont('Microsoft YaHei', 15))
        self.textbox.setGeometry(35, 620, 135, 35)
        self.textbox.setStyleSheet(
            "QLineEdit{color:rgb(0,0,0)}"  # 按键前景色
            "QLineEdit{background-color:rgb(242,242,242)}"  # 按键背景色
            "QLineEdit:hover{background-color:rgb(255,255,255)}"  # 光标移动到上面后的前景色
            "QLineEdit{border: 2px solid rgb(66,66,66);}"  # 边框
        )
        validator = QDoubleValidator(0, 640, 3)
        self.textbox.setValidator(validator)

        # 创建文本框输入确认按钮，并将按钮加入到窗口MainWindow中
        self.text_btn = QtWidgets.QPushButton('OK', MainWindow)
        self.text_btn.setFont(QtGui.QFont('Microsoft YaHei', 10))
        self.text_btn.setGeometry(200, 620, 50, 35)
        self.text_btn.setStyleSheet(
            "QPushButton{color:rgb(255,255,255)}"
            "QPushButton{background-color:rgb(124,179,66)}"
            "QPushButton{border: 2px solid rgb(100,100,100)}"
            "QPushButton:hover{background-color:rgb(104,159,56)}"
            "QPushButton:pressed{background-color:rgb(51,105,30)}")

        # 创建重置按钮
        self.clear_btn = QtWidgets.QPushButton('Reset', MainWindow)
        self.clear_btn.setFont(QtGui.QFont('Microsoft YaHei', 9))
        self.clear_btn.setGeometry(500, 640, 60, 25)
        self.clear_btn.setStyleSheet(
            "QPushButton{color:rgb(80,80,80)}"
            "QPushButton{background-color:rgb(190,190,190)}"
            "QPushButton{border: 2px solid rgb(130,130,130)}"
            "QPushButton:hover{background-color:rgb(150,150,150)}"
            "QPushButton:pressed{background-color:rgb(130,130,130)}")

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Voice Assistant"))

