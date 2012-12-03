#!/usr/bin/python

#
# IMPORTS
#
from M2Crypto import RSA

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
    
    @rtype: dict
    @returns: pair of keys
    """
    # try to create key
    try:
        keys = RSA.gen_key(1024, 65537, lambda x: None)
    
    # issue to save keys: report
    except Exception:
        print "Cannot create key. Aborting."
    
    return { 
            "private": keys,
            "public": keys.pub()
    }
# createKey()

def loadPublicKey(rsaNumbers):
    """
    Loads the public key with given e and n

    @type  rsaNumbers: tuple
    @param rsaNumbers: e and n

    @rtype: object
    @returns: key instance
    """
    # try to load key
    try:
        publicKey = RSA.new_pub_key(rsaNumbers)
    
    except Exception:
        return False

    return publicKey
# loadPublicKey()
