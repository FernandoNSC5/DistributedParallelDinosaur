##########################################################
##.....................__    DATA SERVICE               ##
##.................../ *_)                              ##
##......... _,—-,  _/../     Universidade de Taubaté    ##
##......../............)     Sistemas Distribuidos      ##
##......_/…(….)...(…../      9º Período                 ##
##....../...|_|–...|_|                                  ##
##########################################################
#					 SERVER SIDE						##
##########################################################

import socket, pickle

class server():

	##########################################################
	#					 SERVER SIDE						##
	##########################################################
	def __init__(self):

		print("Initializing server...")

		#Defining static var
		self.SERVER_STATUS = True
		self.BUFFER_LENGTH = 512
		self.HOST = ""
		self.PORT = 5220

		try:
			#Initializing socket sys
			self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

			#criating bind connection
			self.soc.bind((self.HOST, self.PORT))

			#listening to the selected port
			self.soc.listen(1)

			print("Server: Successfully connected")

		except Exception as e:
			print("An error ocurred!\n\tError: " + str(e) + "\n\tclass: server -> server")

		#Listenner loop process
		while True:
			try:
				self.selection()
			except Exception as e:
				print("An error ocurred while processing request")
				break

	##########################################################
	#					 	METHODS							##
	##########################################################
	def selection(self):
		#Accepting connection
		self.conn, self.addr = self.soc.accept()
		print("Server: Request from: " + str(self.addr))

		try:

			self.rcData = self.conn.recv(self.BUFFER_LENGTH)

			if not self.rcData:
				return "";

			#If rcData == 1, server reciving a PING instruction
			if self.rcData == 1:
				print("Server: Returning server status: " + str(self.SERVER_STATUS))
				self.conn.sendall(self.SERVER_STATUS)
				self.conn.close()
				return

			#Descompressing data with Pickle
			self.recData = pickle.loads(self.rcData)

			r = self.processData(self.recData)

			#Returning processed data
			self.conn.sendall(r)

		finally:
			self.conn.close()

	def processData(self, vet):
		m = 0
		for i in vet:
			if i > m:
				m = i
		return m

##########################################################
##						INITING							##
##########################################################
var = server()