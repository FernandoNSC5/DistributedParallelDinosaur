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

#PyQT
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication, QMessageBox, QLineEdit, QWidget, QLabel, QGridLayout, QRadioButton, QComboBox, QMessageBox
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QFont, QPen, QIntValidator

#UNITAU stuff
import data as dt

class App(QMainWindow):

	def __init__(self):
		super().__init__()
		self.DATA_MODULE = dt.Data()
		self.NUM_SERVER = self.DATA_MODULE.getIpListLength()
		self.IP_LIST = self.DATA_MODULE.getIpList()
		self.PORTS_LIST = self.DATA_MODULE.getPorts()
		self.BUFFER_LENGHT = 512

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
		#self.searchBtn.clicked.connect(self.process)

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
		printf("Creating connection")
		#Creating Connection
		soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		
		#List of avaliable servers
		avaliableIp = []
		
		#PING Loop
		for i in self.IP_LIST:
			#1 -> Server avaliable	
			try:
				print("Opening connection IP: "+str(i))
				#With makes sure soc.close() happens
				soc.connect(i, self.PORTS[0])
				#Sends data to current IP
				print("Sending PING")
				soc.sendall(1)
				#Gets response
				self.ipResp = int(soc.recv(self.BUFFER_LENGHT))
				print("Server Response: " + str(ipResp))

				if ipResp == 1:
					self.avaliableIp.append(i)

			finally:
				print("Final avaliable IP list: " + str(self.avaliableIp))
				soc.close()

			#Getting splited vector
			entryVector = vetSegregation()
			#Fragmentating main vector
			subVectorList = vectorFragmentation(entryVector, avaliableIp.size())

			#All ANSWER-RESPONSES list
			answers = []

			#Sending fracments
			#Connecting in each ip
			aux = 0
			for i in self.avaliableIp:
				try:
					print("Creating connection: Ip: " + str(i))
					soc.connect(i, self.PORTS[aux])
					
					#Creating serializable - fragment based
					currentData = pickle.dumps(subVectorList[aux])

					#sending data to current IP
					answers.append(int(soc.recv(self.BUFFER_LENGHT)))

					aux += 1
			
				finally:
					print("Closing connections")
					soc.close()

			#Getting max value on responses
			maxValue = max(answers)

			self.responseLine.setText("Max value: " + str(maxValue))
			self.update()

##########################################################
##						METHODS							##
##########################################################
#VectorFragmentation(List vet, int size (of IP list))
def vectorFragmentation(self, vet, size):
	#Number of vet fragments
	numOfFrag = int(size(vet)/size)

	#Creating sub-vet fragments
	frag = []
	aux = 0
	for i in range(numOfFrag):
		if i == numOfFrag-1:
			frag.append(vet[numOfFrag*i : size(vet)])
			return frag

		frag.append(vet[numOfFrag*i : numOfFrag*(i+1)])

def vetSegregation(self):
	#This method will read VECTORLINE field on screen,
	#get the vector string and convert it to a list
	#splited by SPACE characteres
	vet = self.vectorLine.currentText().split()
	count = 0
	for i in vet:
		vet[i] = int(i)
		count += 1
	return vet

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