#!/usr/bin/python

#
# IMPORTS
#
from Crypto import Random
from Crypto.PublicKey import RSA

import cPickle


#
# CONSTANTS
#


#
# CODE
#
def createKey():
    """
    Creates a private and public key
    
    @rtype: object
    @returns: key object
    """
    # try to create key
    try:
        privateKey = RSA.generate(1024, Random.new().read)
    
    # issue to save keys: report
    except Exception:
        print "Cannot create key. Aborting."
    
    return privateKey
# createKey()

def loadKey(key = None):
    """
    Reads the key

    @type  key: basestring
    @param key: key pickle

    @rtype: object
    @returns: key object on success
    """
    # try to read keys
    try:
        private = cPickle.loads(key)

    # any problem: report
    except Exception:
        print "The key cannot be loaded. Aborting."

    # return pair of keys
    return private
# loadKeys()

def pickleKey(key):
    """
    Creates a pickle

    @type  key: key instance
    @param key: private key

    @rtype: cPickle instance
    @returns: key
    """
    # try to pickle key
    try:
        return cPickle.dumps(key)
    except Exception:
        pass
# pickleKey()

