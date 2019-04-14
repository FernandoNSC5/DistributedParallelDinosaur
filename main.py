##########################################################
##.....................__    DATA SERVICE               ##
##.................../ *_)                              ##
##......... _,—-,  _/../     Universidade de Taubaté    ##
##......../............)     Sistemas Distribuidos      ##
##......_/…(….)...(…../      9º Período                 ##
##....../...|_|–...|_|                                  ##
##########################################################
##					GENERAL INFO						##
##########################################################
## GROUP												##
## 	Fernando Nogueira da Silva Costa					##
## 	Gabriel Ferrari Carvalho							##
## 	João Pedro Valart									##
## 	Pedro Miranda Bueno dos Reis						##
## 														##
## COLOR SCHEMA											##
## 	BACKGROUND #e1d7bc									##
## 	BORDER     #543138									##
## 	FONT       #678875									##
## 	OTHER	   #373948									##
##########################################################

##########################################################
##						IMPORTS							##
##########################################################
#System
import sys
import asyncio
import time

#PyQT
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication, QMessageBox, QLineEdit, QWidget, QLabel, QGridLayout, QRadioButton, QComboBox, QMessageBox
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QFont, QPen, QIntValidator

#UNITAU stuff
import data as dt
import threadingModule as Thread

class App(QMainWindow):

	def __init__(self):
		super().__init__()
		self.DATA_MODULE = dt.Data()
		self.NUM_SERVER = self.DATA_MODULE.getIpListLength()
		self.IP_LIST = self.DATA_MODULE.getIpList()
		self.PORT = self.DATA_MODULE.getPort()
		self.BUFFER_LENGHT = 128

		#Avaliable Threads
		self.threads = []

		#Destroying Windows Flags
		self.setWindowFlags(
						QtCore.Qt.WA_NoSystemBackground |
						QtCore.Qt.Window |
						QtCore.Qt.CustomizeWindowHint |
						QtCore.Qt.WindowTitleHint |
						QtCore.Qt.WindowCloseButtonHint |
						QtCore.Qt.WindowStaysOnTopHint
						)

		#Input Fields
		searchNum = 0
		searchVector = []

		for i in self.IP_LIST:
			self.threads.append(Thread.clientThread(i, self.PORT))
			self.threads[len(self.threads) -1].start()

		for thread in self.threads:
			thread.join()

		for thread in self.threads:
			if not thread.ping():
				self.threads.remove(thread)

		'''#Initializing Threads
		self.threadsSize = 0
		for i in range(len(self.IP_LIST)):
			self.threads.append(None)
			self.threads[self.threadsSize] = Thread.clientThread(self.IP_LIST[i], self.PORT)
			self.threads[self.threadsSize].start()

			time.sleep(4)

			if self.threads[self.threadsSize].ping():
				self.threadsSize = self.threadsSize + 1
				continue
			else:
				self.threads[self.threadsSize].closeConnection()
				self.threads.pop(self.threadsSize)

		'''


		#PyQT sets
		self.pixmap = QPixmap('images/background.png')
		#self.setWindowIcon(QtGui.QIcon('images/icon.png'))
		self.initUI()

	def initUI(self):
		self.setWindowTitle(self.DATA_MODULE.getTitle())
		self.setGeometry(self.DATA_MODULE.getLeftPixel(), self.DATA_MODULE.getTopPixel(), self.DATA_MODULE.getWidth(), self.DATA_MODULE.getHeight())

		#Close Button
		self.drawKillButton()
		self.drawUI()

		self.show()

	#####################################################
	##				PAINTING EVENTS					   ##
	#####################################################
	def paintEvent(self, e):
		painter = QtGui.QPainter(self)
		loop = asyncio.get_event_loop()
		painter.drawPixmap(self.rect(), self.pixmap)
		painter.setRenderHint(QPainter.Antialiasing, True)

		pen = QtGui.QPen()
		pen.setWidth(3)
		pen.setColor(QtCore.Qt.red)
		pen.setCapStyle(QtCore.Qt.RoundCap)
		pen.setJoinStyle(QtCore.Qt.RoundJoin)
		painter.setPen(pen)

	def drawKillButton(self):
		self.killBtn = QPushButton('X', self)
		self.killBtn.setVisible(True)
		self.killBtn.resize(25,25)
		self.killBtn.move(750,25)
		self.killBtn.setStyleSheet("QPushButton {background-color: #543138}"
				"QPushButton {color: white}"
				"QPushButton {border-radius: 12px}")
		self.killBtn.clicked.connect(self.killAppAction)

	def drawUI(self):
		self.vectorLine = QLineEdit(self)
		self.vectorLine.setVisible(True)
		self.vectorLine.resize(600, 40)
		self.vectorLine.move(100, 180)
		self.vectorLine.setPlaceholderText("Input Vector: 1 2 3 4 5 ...")
		self.vectorLine.setStyleSheet("QLineEdit {color: #678875}"
						"QLineEdit {font-size: 15px}"
						"QLineEdit {font-family: Calibri Light}"
						"QLineEdit {border-radius: 8px}"
						"QLineEdit:disabled {background-color: #DBDADA}"
						"QLineEdit:disabled {color: #CD7054}")


		self.searchBtn = QPushButton("Search", self)
		self.searchBtn.setVisible(True)
		self.searchBtn.move(520, 240)
		self.searchBtn.resize(180, 40)
		self.searchBtn.setStyleSheet("QPushButton {background-color: #c88770}"
						"QPushButton {color: white}"
						"QPushButton {border-radius: 12px}"
						"QPushButton:pressed {background-color: #2c3e50}"
						"QPushButton:pressed {border-style: inset}"
						"QPushButton:hover {background-color: #34495e}"
						"QPushButton:disabled {background-color: grey}"
						"QPushButton:disabled {color: white}")
		self.searchBtn.clicked.connect(self.process)

		self.responseLine = QLabel(self)
		self.responseLine.setText("Server Status: " + "none")
		self.responseLine.resize(400, 20)
		self.responseLine.move(280, 300)
		self.responseLine.setVisible(True)
		self.responseLine.setStyleSheet("QLabel {color: #678875}"
						"QLabel {font-size: 20px}"
						"QLabel {font-family: Calibri Light}")

	#####################################################
	##				PYTHON SLOTS					   ##
	#####################################################
	@pyqtSlot()
	def killAppAction(self):
		sys.exit()

	@pyqtSlot()
	def process(self):

		#Get data inputed on UI
		dt = self.vectorLine.text()

		if dt == "SHUTDOWN":
			for i in self.threads:
				i.closeConnection()
			self.responseLine.setText("Connection ended. Reestart software")
			self.update()
			return

		#Creates sub-vectors
		dt = list(map(int, dt.split()))
		print("Vector fragmentation: " + str(self.vectorFragmentation(dt, len(self.threads))))
		vectorOfSubvectors = self.vectorFragmentation(dt, len(self.threads))

		resp = dt[0]
		for i in range(len(self.threads)):
			resp = max(resp, int(self.threads[i].sendData(" ".join(str(x) for x in vectorOfSubvectors[i]))))

		self.responseLine.setText("Max value: " + str(resp))
		self.update()

	##########################################################
	##						METHODS							##
	##########################################################
	#VectorFragmentation(List vet, int size (of IP list))
	def vectorFragmentation(self, vet, size):

		#Number of vet fragments
		numOfFrag = int(len(vet)/size)

		#Creating sub-vet fragments
		frag = []
		aux = 0
		for i in range(numOfFrag):
			if i == numOfFrag-1:
				frag.append(vet[numOfFrag*i : len(vet)])
				return frag

			frag.append(vet[numOfFrag*i : numOfFrag*(i+1)])

##########################################################
##						INITING							##
##########################################################
if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = App()
	ex.resize(ex.pixmap.width(), ex.pixmap.height())
	ex.move(500,450)
	ex.setFixedSize(ex.size())
	ex.update()
	sys.exit(app.exec_())