from enum import Enum
import os
import pickle
import platform
import socket
import struct
import sys
import threading
import time

from aescs import AESCipher

class SecureSocket:
    """Chat server class to handle chat server interactions"""

    def __init__(self, socket, cipher, key, iv):
        """constructor for chat client"""
        self._socket = socket
        self._cipher = cipher
        self._key = key
        self._iv = iv
        self._aescs = AESCipher(key, iv)
        self._aescs.init_suites()
        
    def init_aescs(self):
        self._aescs = AESCipher(self._key, self._iv)
        self._aescs.init_suites()
        
    def send_message(self, message, encrypt):
        """ breaks message into 16 byte chunks and sends them decrypted """
        messageBytes = pickle.dumps(message)

        if encrypt and self._cipher != "none":
            messageBytes = self.encrypt(messageBytes)

            messageLen = len(messageBytes)
            # need to calculate after message encoding, padding and encryption
            header = struct.pack("IIII", messageLen, messageLen, messageLen, messageLen)
            header = self.encrypt(header)            
        else:
            messageLen = len(messageBytes)
            header = struct.pack("IIII", messageLen, messageLen, messageLen, messageLen)
            
        self._socket.sendall(header)
        self._socket.sendall(messageBytes)

            
    def recv_message(self, decrypt=True):
        """ receives an encrypted message, decrypts it, and returns the message object """
    
        if decrypt and self._cipher != "none":
            header = self.recvall(32) # encrypted header gets padding
            header = self.decrypt(header)
        else:
             header = self.recvall(16) 
            
        messageSize = self.get_msg_size(header)
        messageBytes = self.recvall(messageSize)
        
        if decrypt:
            messageBytes = self.decrypt(messageBytes)
        
        message = pickle.loads(messageBytes)
        return message

    def send_raw(self, data, encrypt = True):
        """ """
        if encrypt and self._cipher != "none":
            messageBytes = self.encrypt(data)

        self._socket.sendall(messageBytes)


    def recv_raw(self, amount, decrypt = True):
        """ """
        messageBytes = self.recvall(amount)

        if decrypt and self._cipher != "none":
            messageBytes = self.decrypt(messageBytes)

        return messageBytes

    def get_msg_size(self, header):
        """ unpacks header information and returns the length of the message """
        return struct.unpack("IIII", header)[0]
    
    def recvall(self, length):
        """ receives as many bytes as length from socket """
        data = bytes([])
        while len(data) < length:
            packet = self._socket.recv(length - len(data))
            if not packet:
                return None
            data+= packet
        return data
    
    def encrypt(self, data):
        """ encrypts the passed in data and returns the encrypted data """
        if self._cipher != 'none':
            return self._aescs.encrypt(data)
        return data

    def decrypt(self, data):
        """ decrypts the passed in data and returns the decrypted data """
        if self._cipher != 'none':
            return self._aescs.decrypt(data)
        return data

    def set_cipher(self, cipher):
        self._cipher = cipher

    def set_key(self, key):
        self._key = key

    def set_iv(self, iv):
        self._iv = iv

    def close(self):
        try:
            self._socket.close()
        except:
            print("!! Error closing socket", file=sys.stderr)
                                    
    def __del__(self):
        """destructor for chat client"""
        try:
            self._socket.close()
        except:
            print("Error closing socket", file=sys.stderr)


class MessageError(Exception):
    def __init__(self, message):
        self._message = message

    def __str__(self):
        return repr(self._message)

class MessageType(Enum):
    handshake = 0
    read_file = 1
    write_file = 2
    confirmation = 3
    error = 4
    eof = 5

class Message:
    def __init__(self, mType=None, mPayload=None, mCipher=None):
        if mType is None:
            raise MessageError("Object of type 'Message' must be assigned a type.")

        if mPayload is None:
            raise MessageError("Object of type 'Message' cannot have an empty payload.")

        self._type = mType
        self._cipher = mCipher
        self._payload = mPayload

    @property
    def type(self):
        return self._type

    @property
    def payload(self):
        return self._payload

    @property
    def cipher(self):
        return self._cipher
