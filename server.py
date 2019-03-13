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

import socket, pickle, data

class server():

	##########################################################
	#					 SERVER SIDE						##
	##########################################################
	def __init__(self):

		#Initializing data class
		self.DATA_MODULE = data.Data()

		self.SERVER_STATUS = True
		self.BUFFER_LENGTH = self.DATA_MODULE.getBufferLength()
		self.HOST = self.DATA_MODULE.getHostName()
		self.PORT = self.DATA_MODULE.getPort()

		try:

			#Initializing socket sys
			self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

			#Create bind connection
			self.soc.bind(self.HOST, self.SOCKET)

			#Listen to port
			self.soc.listen(1)
			print("Server: Successfully connected to " + self.IP_DEF)

		except Exception as e:
			print("An error ocurred\n\ttype error: " + str(e) + "\n\tclass: server -> serverSide()")