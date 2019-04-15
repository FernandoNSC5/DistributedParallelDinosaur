##########################################################
##.....................__    SERVER SIDE                ##
##.................../ *_)                              ##
##......... _,—-,  _/../     Universidade de Taubaté    ##
##......../............)     Sistemas Distribuidos      ##
##......_/…(….)...(…../      9º Período                 ##
##....../...|_|–...|_|                                  ##
##########################################################
##	        WELCOME TO SERVER SIDE						##
##########################################################

# COMMANDS LIST
#   RECIVE "SHUTDOWN" - Turn off server
#   RECIVE "PING"     - Returns server status

import socket

class server():
    
    def __init__(self):
        
        self.PORT = 3081
        self.BUFFER_LENGTH = 128
        self.HOST = ""
        
        ###############
        #   STATUS
        #
        #   1  - Avaliable
        #   2  - Not avaliable
        #
        self.STATUS = 1
        
        #Initializing server
        self.initServer()
    
    def initServer(self):
        
        print("[INFO] Initializing server...")
        
        try:
            
            soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            soc.bind((self.HOST, self.PORT))
            print("[SERVER] Initialized")
            
            while True:
                
                soc.listen(1)
                print("[SERVER] Listenning...")
                conn, addr = soc.accept()
                print("[SERVER] Request from " + str(addr))
                
                while True:
                    rcData = conn.recv(self.BUFFER_LENGTH).decode()
                    
                    if str(rcData) == "SHUTDOWN":
                        print("[SERVER] Turning off...")
                        break
                    elif str(rcData) == "PING":
                        print("[SERVER] Ping recived from " + str(addr))
                        conn.send(str(self.STATUS).encode())
                        print("[SERVER] Status returned")
                        print("\n")
                        continue
                    else:
                        print("[SERVER] Request from " + str(addr))
                        print("[SERVER] Processing...")
                        opType, rcData = rcData.split("#")
                        if opType == "MAX":
                            resp = self.processMax(str(rcData))
                        elif opType == "MIN":
                            resp = self.processMin(str(rcData))
                        print("[SERVER] Sending response")
                        conn.send(str(resp).encode())
                        print("[INFO] Response sent to " + str(addr))
                    
                    print("\n")
                
                break
        
        except Exception as e:
            print("[ERROR] " + str(e))
            
        finally:
            print("[INFO] Closing connection")
            soc.close()
            
    def processMax(self, data):
        var = list(map(int, data.split()))
        max = var[0]
        for i in var:
            if int(i) > max:
                max = int(i)
        return str(max)
            
    def processMin(self, data):
        var = list(map(int, data.split()))
        min = var[0]
        for i in var:
            if int(i) < min:
                min = int(i)
        return str(min)

s = server()
                
