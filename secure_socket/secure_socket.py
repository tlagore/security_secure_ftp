import os
import pickle
import platform
import socket
import sys
import threading
import time

from message import Message, MessageType
from encryption_lib import EncryptionLib

class SecureSocket:
    """Chat server class to handle chat server interactions"""

    def __init__(self, socket, cipher, key, iv):
        """constructor for chat client"""
        self._socket = socket
        self._cipher = cipher
        self._key = key
        self._iv = iv
       
    def send_message(self, message, n):
        """ breaks message into 16 byte chunks and sends them decrypted """
        messageBytes = pickle.dumps(message)

        header = self.get_msg_size(messageBytes)
        self._socket.send(self.encrypt(header))
        
        i = 0        
        while i < len(messageBytes):
            msg = messageBytes[i:i+16:]
            if msg == b'':
                msg = bytes([0 for x in range(1, 16)])
            self._socket.send(self.encrypt(msg))
            i=i+16

        if (i - 16) < len(messageBytes):
            msg = messageBytes[i-16:len(messageBytes):]
            
            if len(msg) != 16:
                msg = msg + bytes([0 for x in range(len(msg)+1, 16)])
            self._socket.send(self.encrypt(msg))

    def recv_message(self, n):
        messageBytes = bytes([])
        chunk = self.decrypt(self._socket.recv(16))
        messageSize = self.get_header_size(chunk)
        print("Message size will be {0} bytes".format(messageSize))

        chunk = bytes([])
        while len(chunk) + len(messageBytes) != messageSize:
            chunk += self._socket.recv(1)
            if len(chunk) == 16:
                chunk = self.decrypt(chunk)
                messageBytes += chunk
                chunk = bytes([])

        ## if we hit an error later with padding, it could be here... might need to unpad before
        ## decrypting
        if len(chunk) != 16:
            chunk = self.decrypt(chunk)
            messageBytes += chunk

        message = pickle.loads(messageBytes)
        print(message.payload)
        return message

    def send_unencrypted(self, message):
        """ send an unencrypted message """

    def get_header_size(self, header):
        size = 0
        for el in header:
            size += int(el)

        return size
    
    def get_msg_size(self, message):
        """ takes in a serialized message and spreads its size over a 16 byte array """
        header = []
        size = len(message)
        
        if size > 256 * 16:
            print("!! cannot fit a {0} sized message into a 16 byte array")
            return -1
        
        while size > 255:
            header += [255]
            size -= 255

        header += [size]
        header += [0 for x in range(0, 16-len(header))]
        
        return bytes(header)

    def encrypt(self, data):
        """ encrypts the passed in data and returns the encrypted data """
        # TODO: Encrypt the data...
        return data

    def decrypt(self, data):
        """ decrypts the passed in data and returns the decrypted data """
        # TODO: Decrypt the data...
        return data
                                    
    def __del__(self):
        """destructor for chat client"""
        try:
            self._socket.close()
        except:
            print("Error closing socket", file=sys.stderr)
        finally:
            self.three_dots("Exitting")
