##########################################################
##.....................__    THREAD SERVICE             ##
##.................../ *_)                              ##
##......... _,—-,  _/../     Universidade de Taubaté    ##
##......../............)     Sistemas Distribuidos      ##
##......_/…(….)...(…../      9º Período                 ##
##....../...|_|–...|_|                                  ##
##########################################################
#
#	BASIC INFO
#		This lib were create in order to handle
#		multiple TCP connections
#

##########################################################
##						IMPORTS							##
##########################################################
import socket
import asyncio
from threading import Thread

class clientThread(Thread):

	#####################################################
	##	Initialization								   ##
	#####################################################
	def __init__(self, ip, port):

		Thread.__init__(self)
		self.IP = ip
		self.PORT = port
		self.BUFFER_LENGTH = 128

	# Starting connection with server
	def run(self):
		f = True
		print("[+] Thread added for " + str(self.IP))
		# TCP connection
		self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		try:
			self.soc.connect((self.IP, self.PORT))
		except Exception as e:
			print("[ERROR] run " + str(e))
			f = False

		if f:
			print("[+] New connection established for " + str(self.IP))
		return f

	#Sending pint to self.IP
	def ping(self):
		try:
			print("[INFO] Sending PING to " + str(self.IP))
			self.soc.send("PING".encode())
			print("sended")
			resp = self.soc.recv(self.BUFFER_LENGTH).decode()

			if str(resp) == "1":
				print("[SERVER] " + str(self.IP) + " is avaliable")
				return True
			else:
				print("[SERVER] " + str(self.IP) + " is NOT avaliable")
				return False
		except Exception as e:
			print("[ERROR] ping " + str(e))
			raise e

	# Sends sub-vector to process on self.IP
	def sendData(self, data):

		if data == None or data == "" or not data:
			print("[WARNING] Empty data")
			return

		try:

			print("[INFO] Sending data to " + str(self.IP))
			self.soc.send(data.encode())
			print("[INFO] Data sent")
			resp = self.soc.recv(self.BUFFER_LENGTH).decode()
			print("[INFO] Server responded")
			return resp

		except Exception as e:
			print("[ERROR] " + str(e))
			return

	# Closes Connection
	def closeConnection(self):
		self.sendData("SHUTDOWN")
		self.soc.close()
		print("[-] Connection with " + str(self.IP) + " destroyed")
		return True