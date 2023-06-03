#/var/folders/m4/g0qpzww10fx569x0_1n283300000gn/
import json
import os
from random import randint

import requests
from PyQt6.QtWidgets import *
from PyQt6.QtCore import QThread,pyqtSignal
from PyQt6 import uic
from time import sleep
from Processors.App import StartApp
count = -1
class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        uic.loadUi("DATA/gmail_outlook.ui", self)
        self.pushButton = self.findChild(QPushButton,'pushButton')
        self.pushButton.clicked.connect(self.start)
        self.pushButton_3 = self.findChild(QPushButton,'pushButton_3')
        self.pushButton_3.clicked.connect(self.dialogFiles)
        self.tableWidget = self.findChild(QTableWidget,'tableWidget')
        self.spinBox_2 = self.findChild(QSpinBox,'spinBox_2')
        self.checkBox = self.findChild(QCheckBox,'checkBox')
        self.show()
        self.childThread = {}

    def dialogFiles(self):
        try:
            self.fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "Text Files (*.txt)")
            self.listAccounts = open(self.fileName,'r',encoding='utf8').readlines()
            self.tableWidget.setRowCount(len(self.listAccounts))
            for i in range (len(self.listAccounts)):
                self.tableWidget.setItem(i, 0, QTableWidgetItem(self.listAccounts[i].split('|')[0]))
        except:pass

    def createTable(self,index_row,index_colum,text):
        # Row count
        self.tableWidget.setItem(index_row, index_colum, QTableWidgetItem(text))


    def start(self):
        for i in range(int(self.spinBox_2.value())):
            self.childThread[i] = StartQthread(index=i)
            self.childThread[i].listAccounts = self.listAccounts
            self.childThread[i].checkBox = self.checkBox
            #self.childThread[i].spinBox = self.spinBox
            self.childThread[i].start()
            self.childThread[i].tableStatus.connect(self.createTable)
class StartQthread(QThread):
    tableStatus = pyqtSignal(int,int,str)
    def __init__(self,index = 0):
        super(StartQthread, self).__init__()
        self.index = index
        self.configs = open(os.path.join(os.getcwd(),'Data','configs.json'),'r',encoding='utf8').read()
        self.configs = json.loads(self.configs)


    def run(self):
        global count
        # sau đó truyển tham số vào proxy = proxy
        while count < len(self.listAccounts)-1:
            count += 1
            self.count=count
            if self.checkBox.isChecked():
                proxy = self.call_api_proxy(port=40000)
                proxies = proxy
            else:
                proxies = None
            startapp = StartApp(accounts=self.listAccounts,tableStatus=self.tableStatus,index\
                =self.count,index_thread=self.index,proxies=proxies)
            startapp.start()
            startapp.join()


    def call_api_proxy(self,port=40000):

        url = self.configs['api_proxies']+str(port+self.count)
        response = requests.get(url)
        proxy = f'127.0.0.1:{port+self.count}'
        return proxy

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    UiWindow = UI()
    app.exec()