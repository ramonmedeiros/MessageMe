#
# SEARCH PATH ADJUSTMENTS
#
import sys
sys.path.insert(0, '/home/ramon/MessageMe')
 

#
# IMPORTS
#
from cryptFunctions import createKey
from cryptFunctions import loadKey
from cryptFunctions import pickleKey
from listenerSender import Listener
from listenerSender import Sender

import time

#
# CONSTANTS
#
START_CONNECTION = "cabecadedragao"
ACK_CONNECTION = "piolhodecobra"


#
# CODE
#

class MessageHandler():
    """
    Handle messages
    """

    def __init__(self):
        """
        Constructor

        @rtype: None
        @returns: Nothing
        """
        # chat data
        self.__data = []
        
        # create key
        self.__key = None

        # create listener thread
        self.__listener = Listener(self.__data, self.answerConnection, self.__key)
        self.__listener.start()
        self.__listener.join()
    # __init__()

    def connect(self, ip):
        """
        Connect to a computer

        @type  ip: basestring
        @param ip: ip address
         
        @rtype: bool
        @returns: True on success, False otherwise
        """
        # create counters
        counter = 0

        # send connect sinal
        self.sendMessage(START_CONNECTION, ip)

        # wait answer from other server
        while counter < 3:
            lastMessage = self.getLastMessage()
            
            # count one iteraction
            counter += 1
            
            # empty message: continue
            if lastMessage == {}:
                time.sleep(1)
                continue

            # computer answered connection request: share keys
            strippedMessage = lastMessage["message"].strip()
            if len(strippedMessage) == 2 and strippedMessage[0] == ACK_CONNECTION:
                
                # get key
                key = loadKey(strippedMessage[1])
                self.__key = key.publicKey()
                break
    # connect()

    def answerConnection(self, ip):
        """
        Connect to a server

        @type  ip: basestring
        @param ip: ip of computer

        @rtype: bool
        @returns: True on success, False otherwise
        """
        # create key
        key = createKey()

        # create pickle
        pickle = pickleKey(self.__key)

        # send message
        self.sendMessage("%s %s" % (ACK_CONNECTION, pickle), ip)

        # store key
        self.__key = key
    # answerConnection()

    def getLastMessage(self):
        """
        Reads the last message

        @rtype: dict
        @returns: message
        """
        # messages pending on list: return it
        if len(self.__data) > 0:
            return self.__data.pop(0)

        # return empty
        return {}
    # getLastMessage()
    
    def sendMessage(self, message, ip):
        """
        Sends a message

        @type  message: basestring
        @param message: message text

        @type  ips: basestring
        @param ips: ip to send message
        
        @rtype: bool
        @returns: True on success, False otherwise
        """
        # create sender thread
        sender = Sender(message, ip, self.__key)
        return sender.start()
    # sendMessage()

# MessageHandler()
