##########################################################
##.....................__    SERVER SIDE                ##
##.................../ *_)                              ##
##......... _,—-,  _/../     Universidade de Taubaté    ##
##......../............)     Sistemas Distribuidos      ##
##......_/…(….)...(…../      9º Período                 ##
##....../...|_|–...|_|                                  ##
##########################################################
##	             WELCOME TO SERVER SIDE					##
##########################################################

# COMMANDS LIST
#   RECEIVE "SHUTDOWN" - Turn off server
#   RECEIVE "PING"     - Returns server status

import socket

class server():
    
    def __init__(self):
        
        self.PORT = 3000
        self.BUFFER_LENGTH = 128
        self.HOST = ""
        self.listenTimes = 100
        
        ##########################
        #   STATUS               #
        #                        #
        #   1  - Available       #
        #   2  - Not available   #
        #                        #
        ##########################
        self.STATUS = 1
        
        #Initializing server
        self.initServer()
    
    def initServer(self):
        
        print("[INFO] Initializing server...")
        
        try:
            
            soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            soc.bind((self.HOST, self.PORT))
            print("[SERVER] Initialized")
            soc.listen(self.listenTimes)
            timesListened = 0
            while True:
                timesListened += 1
                print("[SERVER] Listenning PORT" + str(self.PORT))
                conn, addr = soc.accept()
                print("[SERVER] Request n° " + str(timesListened))
                print("[SERVER] Requests from " + str(addr))
                
                while True:
                    rcData = conn.recv(self.BUFFER_LENGTH).decode()
                    
                    if str(rcData) == "SHUTDOWN":
                        print("[SERVER] Turning off...")
                        break
                    if str(rcData) == "SHUTDOWNSERVER":
                        print("[SERVER] Turning off...")
                        timesListened = self.listenTimes
                        break
                    elif str(rcData) == "PING":
                        print("[SERVER] Ping received")
                        conn.send(str(self.STATUS).encode())
                        print("[SERVER] Status returned")
                    else:
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
                
                if timesListened == self.listenTimes:
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