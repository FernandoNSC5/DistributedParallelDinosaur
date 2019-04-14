##########################################################
##.....................__    DATA SERVICE               ##
##.................../ *_)                              ##
##......... _,—-,  _/../     Universidade de Taubaté    ##
##......../............)     Sistemas Distribuidos      ##
##......_/…(….)...(…../      9º Período                 ##
##....../...|_|–...|_|                                  ##
##########################################################

class Data():

	#####################################################
	##				USEFULL STUFF					   ##
	#####################################################
	def __init__(self):
		#Socket info
		######################### 	   	     Pi        Oneplus
		self.AVAILABLE_IP_LIST = ["192.168.137.141", "192.168.137.73"]
		self.IP_LIST_LENGTH = len(self.AVAILABLE_IP_LIST)
		#Avaliable ports
		self.PORT = 3102
		self.BUFFER_LENGTH = 128
		self.HOST_NAME = ""
		#PyQT info
		self.LEFT = 10
		self.TOP = 10
		self.WIDTH = 640
		self.HEIGHT = 480
		self.TITLE = "Distributed Parallel Dinosaur"
		

	#####################################################
	##				GETTERS AND SETTER				   ##
	#####################################################
	def getIpList(self):
		return self.AVAILABLE_IP_LIST

	def getIpByIndex(self, index):
		return self.AVAILABLE_IP_LIST[index]

	def getIpListLength(self):
		return self.IP_LIST_LENGTH

	def getPort(self):
		return self.PORT

	def getBufferLength(self):
		return self.BUFFER_LENGTH

	def getHostName(self):
		return self.HOST_NAME

	def getLeftPixel(self):
		return self.LEFT

	def getWidth(self):
		return self.WIDTH

	def getTopPixel(self):
		return self.TOP

	def getHeight(self):
		return self.HEIGHT

	def getTitle(self):
		return self.TITLE