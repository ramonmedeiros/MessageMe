#
# IMPORTS
#
from threading import Thread

import socket
import time


#
# CONSTANTS
#
PORT = 65001
START_CONNECTION = "cabecadedragao"


#
# CODE
#
class Listener(Thread):
    """
    Listen traffic
    """

    def __init__(self, data, startConnection, key = None):
        """
        Constructor

        @type  data: list
        @param data: list with data listened

        @type  startConnection: callable
        @param startConnection: method to answer connection

        @type  key: object
        @param key: key instance

        @rtype: None
        @returns: Nothing
        """
        # call parent
        Thread.__init__(self)

        # store list and file
        self.__data = data
        self.__connection = startConnection
        self.__key = key
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
        serverSocket.bind(("", PORT))

        # wait connection
        while True:

            # get connection
            serverSocket.listen(5)
            clientSocket, address = serverSocket.accept()
            address, port = address

            # read connection
            while True:
             
                # get message and send data
                data = clientSocket.recv(512)

                # user asking to connect: connect
                if data == START_CONNECTION:
                    self.__connection(address)
                    continue

                # data is null: skip
                elif len(data) == 0:
                    continue

                # key not passed: do nothing
                elif self.__key == None:
                    text = data

                # key passed: decrypt message
                else:
                    text = self.__key.decrypt(data)

                # send data
                self.__data.append({ 
                    "message": text, 
                    "time": time.asctime(),
                    "address": address 
                })
    
    # run()
# Listener()
