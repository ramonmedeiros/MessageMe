#
# IMPORTS
#
import socket


#
# CONSTANTS
#


#
# CODE
#
def sendMessage(message, ip, port, cryptMethod = None):
    """
    Listen socket and send data

    @rtype:  list
    @returns: report operation failure
    """
    # create socket
    sendSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # try to send message
    sendSocket.connect((ip, port))

    # key passed: encrypt message
    if cryptMethod == None:
        text = message

    # key not passed: do nothing
    else:
        text = cryptMethod(message, 1)

    # send message
    sendSocket.sendall(text)
    sendSocket.close()
# sendMessage()
