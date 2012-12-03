#
# SEARCH PATH ADJUSTMENTS
#
import sys
sys.path.insert(0, '/home/ramon/MessageMe')
 

#
# IMPORTS
#
from cryptFunctions import createKey
from cryptFunctions import loadPublicKey
from listenerSender import Listener
from listenerSender import sendMessage as send

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

    def __init__(self, receivePort):
        """
        Constructor

        @type  receivePort: int
        @param receivePort: port to listen traffic

        @rtype: None
        @returns: Nothing
        """
        # store vars
        self.__data = []
        self.__cryptMethod = None
        self.__rPort = receivePort
        self.__ip = None
        self.key = False

        # create listener thread
        self.__listener = Listener(self.__data, 
                                   self.__answerConnection,
                                   self.__setPublicKey,
                                   self.__rPort)
        self.__listener.start()
    # __init__()

    def connect(self, ip, port):
        """
        Connect to a computer

        @type  ip: basestring
        @param ip: ip address
         
        @rtype: bool
        @returns: True on success, False otherwise
        """
        # create counters
        self.__ip = ip
        self.__port = port

        # send connect sinal
        self.sendMessage("%s %s" % (START_CONNECTION, self.__rPort))
    # connect()

    def __setPublicKey(self, pubKey):
        """
        Sets publicKey

        @type  pubKey: tuple
        @param pubKey: public key numbers
        
        @rtype: None
        @returns: Nothing
        """
        # create public key
        publicKey = loadPublicKey(pubKey)

        # set crypt methods
        self.__cryptMethod = publicKey.public_encrypt
        self.__listener.setDecryptMethod(publicKey.public_decrypt)
        self.key = True
   # __setPublicKey()

    def __answerConnection(self, ip, port):
        """
        Gives public key to another server to a server

        @type  ip: basestring
        @param ip: ip of computer

        @rtype: bool
        @returns: True on success, False otherwise
        """
        # create keys
        key = createKey()
        
        # set port and ip
        self.__port = port
        self.__ip = ip

        # send message
        e = key["public"][0].encode("base64").replace('\\n', '\n')
        n = key["public"][1].encode("base64").replace('\\n', '\n')
        self.sendMessage("%s %s %s" % (ACK_CONNECTION, e, n))

        # store crypt methods
        self.__cryptMethod = key["private"].private_encrypt
        self.__listener.setDecryptMethod(key["private"].private_decrypt)
        self.key = True
    # __answerConnection()

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
        return False
    # getLastMessage()
    
    def sendMessage(self, message, ip = None, port = None):
        """
        Sends a message

        @type  message: basestring
        @param message: message text

        @rtype: bool
        @returns: True on success, False otherwise
        """
        # no port specified: use stored port
        if port == None:
            port = self.__port

        # no ip specified: use stored ip
        if ip == None:
            ip = self.__ip

        # create sender thread
        send(message, ip, port, self.__cryptMethod)
    # sendMessage()

# MessageHandler()
