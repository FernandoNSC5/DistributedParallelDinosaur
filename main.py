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
## 	João Pedro Silvino Paes								##
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
		self.DATA_MODULE   = dt.Data()
		self.NUM_SERVER    = self.DATA_MODULE.getIpListLength()
		self.IP_LIST       = self.DATA_MODULE.getIpList()
		self.PORT          = self.DATA_MODULE.getPort()
		self.BUFFER_LENGHT = 128

		#Avaliable Threads
		self.threads = []

		#Destroying Windows Flags
		self.setWindowFlags(
						QtCore.Qt.Window |
						QtCore.Qt.CustomizeWindowHint |
						QtCore.Qt.WindowTitleHint |
						QtCore.Qt.WindowCloseButtonHint |
						QtCore.Qt.WindowStaysOnTopHint
						)

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
		self.makeConnection()

	#####################################################
	##				PAINTING EVENTS					   ##
	#####################################################
	def paintEvent(self, e):
		painter = QtGui.QPainter(self)
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


		self.searchMaxBtn = QPushButton("Search Max", self)
		self.searchMaxBtn.setVisible(True)
		self.searchMaxBtn.move(520, 240)
		self.searchMaxBtn.resize(180, 40)
		self.searchMaxBtn.setStyleSheet("QPushButton {background-color: #c88770}"
						"QPushButton {color: white}"
						"QPushButton {border-radius: 12px}"
						"QPushButton:pressed {background-color: #2c3e50}"
						"QPushButton:pressed {border-style: inset}"
						"QPushButton:hover {background-color: #34495e}"
						"QPushButton:disabled {background-color: grey}"
						"QPushButton:disabled {color: white}")
		self.searchMaxBtn.clicked.connect(self.processMax)

		self.searchMinBtn = QPushButton("Search Min", self)
		self.searchMinBtn.setVisible(True)
		self.searchMinBtn.move(320, 240)
		self.searchMinBtn.resize(180, 40)
		self.searchMinBtn.setStyleSheet("QPushButton {background-color: #c88770}"
						"QPushButton {color: white}"
						"QPushButton {border-radius: 12px}"
						"QPushButton:pressed {background-color: #2c3e50}"
						"QPushButton:pressed {border-style: inset}"
						"QPushButton:hover {background-color: #34495e}"
						"QPushButton:disabled {background-color: grey}"
						"QPushButton:disabled {color: white}")
		self.searchMinBtn.clicked.connect(self.processMin)

		self.responseLine = QLabel(self)
		self.responseLine.setText("")
		self.responseLine.resize(400, 20)
		self.responseLine.move(280, 300)
		self.responseLine.setVisible(True)
		self.responseLine.setStyleSheet("QLabel {color: #678875}"
						"QLabel {font-size: 20px}"
						"QLabel {font-family: Calibri Light}")

		self.serverLine = QLabel(self)
		self.serverLine.setText("Offline")
		self.serverLine.resize(200, 20)
		self.serverLine.move(20, 20)
		self.serverLine.setVisible(True)
		self.serverLine.setStyleSheet("QLabel {color: #678875}"
						"QLabel {font-size: 20px}"
						"QLabel {font-family: Calibri Light}")

	#####################################################
	##				PYTHON SLOTS					   ##
	#####################################################
	@pyqtSlot()
	def killAppAction(self):
		self.closeConnections()
		sys.exit()

	@pyqtSlot()
	def processMax(self):
		self.process("MAX")

	@pyqtSlot()
	def processMin(self):
		self.process("MIN")

	##########################################################
	##						METHODS							##
	##########################################################
	#VectorFragmentation(List vet, int size (of IP list))
	def vectorFragmentation(self, vet):
		#Size = number of open threads
		size = len(self.threads)
		#Number of vet fragments
		numOfFrag = int(len(vet)/size)
		#Creating sub-vet fragments
		frag = []
		loopCounter = numOfFrag*size
		for i in range(loopCounter):
			if i == (loopCounter)-1:
				frag.append(vet[numOfFrag*i : len(vet)])
				return frag
			frag.append(vet[numOfFrag*i : numOfFrag*(i+1)])

	#process(string opType (Type of Operation [MAX, MIN]))
	def process(self, opType):
		if(len(self.threads) == 0):
			self.responseLine.setText("No connection.")
			return
		#Get data inputed on UI
		dt = self.vectorLine.text()

		if(len(dt) == 0):
			self.responseLine.setText("No data to proccess.")
			return

		#Creates sub-vectors
		dt = list(map(int, dt.split()))
		vectorOfSubvectors = self.vectorFragmentation(dt)

		resp = dt[0]

		if opType == "MAX":
			typeFunction = max
		elif opType == "MIN":
			typeFunction = min
		else:
			self.responseLine.setText("Type of function error")
			self.update()
			return

		for i in range(len(self.threads)):
			resp = typeFunction(resp, int(self.threads[i].sendData(opType + "#" + " ".join(str(x) for x in vectorOfSubvectors[i]))))

		self.responseLine.setText(opType + " VALUE: " + str(resp))
		self.update()

	def makeConnection(self):
		self.serverLine.setText("Refreshing")
		self.update()
		for IP in self.IP_LIST:
			self.threads.append(Thread.clientThread(IP, self.PORT))
			self.threads[-1].start()

		for thread in self.threads:
			thread.join(1.5)

		j = 0
		while j < len(self.threads):
			try:
				self.threads[j].ping()
				j += 1
			except Exception:
				self.threads.pop(j)
		
		if(len(self.threads)):
			self.serverLine.setText("Online")
		else:
			self.serverLine.setText("Offline")
		self.update()

	def closeConnections(self):
		while len(self.threads):
			self.threads[0].closeConnection()
			self.threads.pop(0)

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