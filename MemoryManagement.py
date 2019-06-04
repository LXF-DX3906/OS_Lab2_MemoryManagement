from PyQt5 import QtWidgets, QtGui, QtCore, uic
from UI import Ui_MainWindow
import sys
from functools import partial
import base64
from memory_pic import *
import re
sys.dont_write_bytecode = True

def get_pic(pic_code, pic_name):
    image = open(pic_name, 'wb')
    image.write(base64.b64decode(pic_code))
    image.close()
get_pic(two_ico, "two.ico")

class myWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(myWindow, self).__init__()
        self.myCommand = " "
        self.setWindowIcon(QtGui.QIcon('two.ico'))
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.firstFit_bar.triggered.connect(self.firstFitbar_recognize)  # firstFit模式触发
        self.ui.bestFit_bar.triggered.connect(self.bestFitbar_recognize)  # bestFit模式触发
        self.ui.text_btn.clicked.connect(self.text_changed)  # 文本框输入确认按钮连接文本处理函数
        self.ui.textbox.returnPressed.connect(self.text_changed)  # 文本框输入响应enter键
        self.ui.clear_btn.clicked.connect(self.clear)  # Reset按钮连接重置内存空间函数

        for i in range(0, 64):
            self.ui.btnGroup[i].clicked.connect(
                partial(self.addNode, 10*(i+1)))
        self.isbestFit = False  # 标志是否选择bestFit识别
        self.workNumber = 0  # 作业个数
        self.nodeList = []  # 结点链表
        # 初始化，将640k视为一个空结点
        self.nodeList.insert(0, {'number': -1,  # 非作业结点
                                 'start': 0,  # 开始为0
                                 'length': 640,  # 长度为640
                                 'isnull': True})  # 空闲
        # 加入一个非作业btn
        self.nodeList[0]['btn'] = self.addButton(self.nodeList[0])

    # firstFit从未选状态转变为已选状态时会触发firstFitbar_recognize函数
    def firstFitbar_recognize(self):
        self.clear()  # 重置内存空间
        self.ui.firstFit_bar.setChecked(True)
        self.ui.bestFit_bar.setChecked(False)
        self.ui.firstFit_action.setText(" √  First fit  ")
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        self.ui.firstFit_action.setFont(font)
        self.ui.firstFit_action.setStyleSheet(
            "QLabel { color: rgb(255,255,255);  /*字体颜色*/ \
                background-color:rgb(51,105,30);\
                }"
            "QLabel:hover{  background-color:rgb(51,105,30);/*选中的样式*/ \
                }"
        )
        self.ui.bestFit_action.setText("     Best fit  ")
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        self.ui.bestFit_action.setFont(font)
        self.ui.bestFit_action.setStyleSheet(
            "QLabel { color: rgb(225,225,225);  /*字体颜色*/ \
                background-color:rgb(124,179,66);\
                }"
            "QLabel:hover{ background-color:rgb(51,105,30);/*选中的样式*/ \
                            }"
        )
        self.isbestFit = False

    # bestFit从未选状态转变为已选状态时会触发bestFitbar_recognize函数
    def bestFitbar_recognize(self):
        self.clear()  # 重置内存空间
        self.ui.bestFit_bar.setChecked(True)
        self.ui.firstFit_bar.setChecked(False)
        self.ui.firstFit_action.setText("     First fit  ")
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        self.ui.firstFit_action.setFont(font)
        self.ui.firstFit_action.setStyleSheet(
            "QLabel { color: rgb(225,225,225);  /*字体颜色*/ \
                background-color:rgb(124,179,66);\
                }"
            "QLabel:hover{ background-color:rgb(51,105,30);/*选中的样式*/ \
                            }"
        )
        self.ui.bestFit_action.setText(" √  Best fit  ")
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        self.ui.bestFit_action.setFont(font)
        self.ui.bestFit_action.setStyleSheet(
            "QLabel { color: rgb(255,255,255);  /*字体颜色*/ \
                background-color:rgb(51,105,30);\
                }"
            "QLabel:hover{  background-color:rgb(51,105,30);/*选中的样式*/ \
                }"
        )
        self.isbestFit = True

    # 重置内存空间函数
    def clear(self):
        self.workNumber = 0  # 作业个数置0
        self.nodeList.insert(0, {'number': -1,  # 非作业结点
                                 'start': 0,  # 开始0
                                 'length': 640,  # 长度640
                                 'isnull': True})  # 空闲
        # 加入一个非作业btn
        self.nodeList[0]['btn'] = self.addButton(self.nodeList[0])
        size = len(self.nodeList)
        for i in range(1, size):
            self.nodeList.pop()

    # 寻找首次适应算法添加结点的位置
    def findFirstNode(self, length):
        self.targetNumber = -1
        for i in range(0, len(self.nodeList)):
            # 如果结点i为空闲
            if self.nodeList[i]['isnull'] and self.nodeList[i]['length'] >= length:
                self.targetNumber = i
                return self.targetNumber
        return -1

    # 寻找最佳适应算法添加结点的位置
    def findBestNode(self, length):
        self.min = 650
        self.targetNumber = -1
        for i in range(0, len(self.nodeList)):
            # 如果结点i为空闲
            if self.nodeList[i]['isnull'] and (self.min > self.nodeList[i]['length'] >= length):
                self.min = self.nodeList[i]['length']
                self.targetNumber = i
        return self.targetNumber

    # 添加结点
    def addNode(self, length):
        if self.isbestFit:
            i = self.findBestNode(length)
        else:
            i = self.findFirstNode(length)
        if i >= 0:
            self.workNumber += 1  # 作业数量+1
            if self.nodeList[i]['length'] > length:
                # 在该结点后插入新的作业结点
                self.nodeList.insert(i+1, {'number': self.workNumber,  # 作业workNumber
                                           'start': self.nodeList[i]['start'],  # 开始为结点i的开始
                                           'length': length,  # 长度
                                           'isnull': False})  # 不空闲
                # 加入一个作业btn
                self.nodeList[i+1]['btn'] = self.addButton(self.nodeList[i+1])
                self.nodeList[i+1]['btn'].clicked.connect(
                    partial(self.deleteNode, self.nodeList[i+1]['number']))
                # 将剩下的部分置为空白结点
                self.nodeList.insert(i+2, {'number': -1,  # 非作业结点
                                           'start': self.nodeList[i+1]['start']+length,  # 开始为i+1的开始+length
                                           'length': self.nodeList[i]['length']-length,  # 长度为结点i的长度-length
                                           'isnull': True})  # 空闲
                # 加入一个非作业btn
                self.nodeList[i+2]['btn'] = self.addButton(self.nodeList[i+2])
                # 删除结点i
                del self.nodeList[i]
            # 空闲结点i的长度等于所需长度
            elif self.nodeList[i]['length'] == length:
                # 在该结点后插入新的作业结点
                self.nodeList.insert(i + 1, {'number': self.workNumber,  # 作业workNumber
                                             'start': self.nodeList[i]['start'],  # 开始为结点i的开始
                                             'length': length,  # 长度
                                             'isnull': False})  # 不空闲
                # 插入一个作业btn
                self.nodeList[i + 1]['btn'] = self.addButton(self.nodeList[i+1])
                self.nodeList[i + 1]['btn'].clicked.connect(
                    partial(self.deleteNode, self.nodeList[i + 1]['number']))
                # 删除结点i
                del self.nodeList[i]

    # 删除作业结点
    def deleteNode(self, workNumber):
        self.current = -1
        # 寻找目标删除结点
        for i in range(0, len(self.nodeList)):
            if self.nodeList[i]['number'] == workNumber:
                self.current = i
                break
        # 找到目标删除结点
        if self.current != -1:
            # 前后都无空闲结点
            if (self.current == 0 or bool(1-self.nodeList[self.current - 1]['isnull'])) \
                    and (self.current == len(self.nodeList) - 1 or bool(1-self.nodeList[self.current + 1]['isnull'])):
                self.nodeList.insert(self.current + 1, {'number': -1,  # 非作业结点
                                                        # 开始为self.current结点的开始
                                                        'start': self.nodeList[self.current]['start'],
                                                        # 长度为结点self.current长度
                                                        'length': self.nodeList[self.current]['length'],
                                                        'isnull': True})  # 空闲
                # 加入一个非作业btn
                self.nodeList[self.current + 1]['btn'] = self.addButton(self.nodeList[self.current+1])
                del self.nodeList[self.current]
            else:
                # 结点非头结点且其前一个结点是空闲结点
                if self.current-1 >= 0 and self.nodeList[self.current-1]['isnull']:
                    # 将两部分合为一个空白结点
                    self.nodeList.insert(self.current + 1, {'number': -1,  # 非作业结点
                                                             # 开始为self.current-1结点的开始
                                                             'start': self.nodeList[self.current - 1]['start'],
                                                             # 长度为结点self.current-1的长度+结点self.current的长度
                                                             'length': self.nodeList[self.current-1]['length']
                                                                       + self.nodeList[self.current]['length'],
                                                             'isnull': True})  # 空闲
                    # 加入一个非作业btn
                    self.nodeList[self.current + 1]['btn'] = self.addButton(self.nodeList[self.current+1])
                    # 删除原来两结点
                    del self.nodeList[self.current-1]
                    # 删除current
                    del self.nodeList[self.current-1]
                    self.current -= 1
                # 结点非尾结点且其后一个结点为空白结点
                if self.current < len(self.nodeList)-1 and self.nodeList[self.current+1]['isnull']:
                    # 将两部分合为一个空白结点
                    self.nodeList.insert(self.current + 2, {'number': -1,  # 非作业结点
                                                            # 开始为self.current结点的开始
                                                           'start': self.nodeList[self.current]['start'],
                                                           # 长度为结点self.current的长度+结点self.current+1的长度
                                                           'length': self.nodeList[self.current]['length']
                                                                     + self.nodeList[self.current + 1]['length'],
                                                           'isnull': True})  # 空闲
                    # 加入一个非作业btn
                    self.nodeList[self.current + 2]['btn'] = self.addButton(self.nodeList[self.current+2])
                    # 删除原来两结点
                    del self.nodeList[self.current]
                    # 删除current+1
                    del self.nodeList[self.current]

    # 加入作业
    def addButton(self, node=[]):
        if node['isnull']:  # 空闲结点按钮
            btn = QtWidgets.QPushButton(str(node['length'])+'k', self)
            btn.setFont(QtGui.QFont('Microsoft YaHei', node['length']/42 + 5))
            btn.setGeometry(380, 30+node['start'], 100, node['length'])
            btn.setStyleSheet(
                "QPushButton{color:rgb(150,150,150)}"
                "QPushButton{background-color:rgb(240,240,240)}"
                "QPushButton{border: 1.5px solid rgb(66,66,66);}"
            )
            btn.setVisible(True)
        else:       # 作业结点按钮
            btn = QtWidgets.QPushButton('P'+str(node['number'])+':\n'+str(node['length'])+'k', self)
            btn.setFont(QtGui.QFont('Microsoft YaHei', node['length'] / 42 + 5))
            btn.setGeometry(380, 30 + node['start'], 100, node['length'])
            btn.setStyleSheet(
                "QPushButton{color:rgb(1,0,0)}"
                "QPushButton{background-color:rgb(124,179,66)}"
                "QPushButton:hover{background-color:rgb(210,210,210)}"
                "QPushButton:pressed{background-color:rgb(200,200,200)}"
                "QPushButton{border: 1.5px solid rgb(66,66,66);}"
            )
            btn.setVisible(True)
        return btn

    #文本处理函数
    def text_changed(self):
        if self.ui.textbox.text() == '':
            self.content = 0
        else:
            self.content = 0
            if ('.' not in self.ui.textbox.text()):
                self.content = int(self.ui.textbox.text())
                #self.content = int("".join(list(filter(str.isdigit, self.ui.textbox.text()))))
            else:
                self.content = float(self.ui.textbox.text())
        print(self.content)
        self.ui.textbox.setText('')
        if self.content <= 640:
            self.addNode(self.content)



if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    application = myWindow()
    application.show()
    sys.exit(app.exec_())


