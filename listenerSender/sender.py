#
# IMPORTS
#
from threading import Thread

import socket


#
# CONSTANTS
#
SEND_PORT = 65000


#
# CODE
#
class Sender(Thread):
    """
    Listen traffic
    """

    def __init__(self, message, ip, key = None):
        """
        Constructor

        @type  message: basestring
        @param message: message to be sent

        @type  senders: list
        @param senders: list of ips to be sent
 
        @type  key: callable
        @param key: key object

        @rtype: None
        @returns: Nothing
        """
        # call parent
        Thread.__init__(self)

        # store list and file
        self.__message = message
        self.__sender = ip
        self.__key = key
    # __init__()

    def run(self):
        """
        Listen socket and send data

        @rtype:  list
        @returns: report operation failure
        """
        # create socket
        sendSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # try to send message
        try:
            sendSocket.connect((self.__sender, SEND_PORT))

            # key passed: encrypt message
            if self.__key != None:
                text = self.__key.encrypt(self.__message, None)
            
            # key not passed: do nothing
            else:
                text = self.__message

            # send message
            sendSocket.sendall(text)
            sendSocket.close()

        # cannot send message: pass
        except Exception:
            return False

        return True
    #  run()
# Sender()
