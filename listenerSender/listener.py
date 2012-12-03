#
# IMPORTS
#
from threading import Thread

import socket
import time

#
# CONSTANTS
#
START_CONNECTION = "cabecadedragao"
ACK_CONNECTION = "piolhodecobra"

#
# CODE
#
class Listener(Thread):
    """
    Listen traffic
    """

    def __init__(self, data, startConnection, setPublicKey, port):
        """
        Constructor

        @type  data: list
        @param data: list with data listened

        @type  startConnection: callable
        @param startConnection: method to answer connection

        @type  setPublicKey: callable
        @param setPublicKey: method to set public key

        @type  port: int
        @param port: port to listen traffic

        @rtype: None
        @returns: Nothing
        """
        # call parent
        Thread.__init__(self)

        # store list and file
        self.__data = data
        self.__connection = startConnection
        self.__setPubKey = setPublicKey
        self.__cryptMethod = None
        self.__port = port
    # __init__()

    def run(self):
        """
        Listen socket and send data

        @rtype:  None
        @returns: Nothing
        """
        # create socket and list at specific port
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serverSocket.settimeout(None)
        serverSocket.bind(("", self.__port))

        # read connection
        while True:
        
            # get connection
            serverSocket.listen(1)
            clientSocket, address = serverSocket.accept()
            address, port = address

            # set text
            text = None
            
            # get message and send data
            data = clientSocket.recv(1024)

            # data is null: skip
            if len(data) == 0 or data == "":
                time.sleep(1)
                continue

            # data has more than 1 word: parse if it is a command
            splitData = data.split()
            if len(splitData) > 1 :
                
                # connection requested: pass arguments
                if splitData[0] == START_CONNECTION:
                    self.__connection(address, int(data.split()[1]))
                    continue
                
                # public key sent: receive and set it
                if splitData[0] == ACK_CONNECTION:
                    e = splitData[1].decode("base64").replace('\\n', '\n')
                    n = '\n'.join(splitData[2:]).decode("base64").replace('\\n', '\n')
                    rsaNumbers = (e, "" + n)
                    self.__setPubKey(rsaNumbers)
                    continue

            # key not passed: do nothing
            if self.__cryptMethod == None:
                text = data

            # key passed: decrypt message
            else:
                text = self.__cryptMethod(data, 1)

            # cannot get text: skip
            if text == None:
                continue
                
            # send data
            self.__data.append({ 
                "message": text, 
                "time": time.asctime(),
                "address": address 
            })
    # run()

    def setDecryptMethod(self, decryptMethod):
        """
        Sets decrypt method

        @type  decryptMethod: callable
        @param decryptMethod: decrypt method

        @rtype: None
        @returns: Nothing
        """
        # set it
        self.__cryptMethod = decryptMethod
    # setDecryptMethod()
# Listener()
