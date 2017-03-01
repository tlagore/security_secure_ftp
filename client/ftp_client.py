from getpass import getpass
import os
import pickle
import platform
import socket
import sys
import threading
import time

from message import Message, MessageType

class FTPClient:
    """Chat server class to handle chat server interactions"""

    def __init__(self, host, port, command, filename, cipher, key):
        """constructor for chat client"""
        print("!! Client starting. Arguments: ".format(host, port))
        print("!! \thost: {0}".format(host))
        print("!! \tport: {0}".format(port))
        print("!! \tcommand: {0}".format(command))
        print("!! \tfilename: {0}".format(filename))
        print("!! \tcipher: {0}".format(cipher))
        print("!! \tkey: {0}".format(key))

        self._host = host
        self._port = port
        self._command = command
        self._filename = filename
        self._cipher = cipher
        self._key = key
        self._iv = self.gen_nonce()

        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((host, port))
        self.worker()

    def worker(self):
        """ worker thread for ftp_client """
        response = self.handshake()

        print("{0} {1}".format(response.type, response.payload))
        if response.payload == True:
            if self._command == "read":
                self.read()
            elif self._command == "write":
                self.write()
        else:
            print("!! Server denied connection. Received false confirmation after handshake")
        
    def handshake(self):
        """ generates an initialization vector for the server waits for confirmation """
        message = Message(mType=MessageType.handshake, mPayload=self._iv, mCipher=self._cipher)
        self._socket.send(pickle.dumps(message))
        response = self.recv_message()
        return response

    def read(self):
        """ reads a file from the server"""
        print("Read!")
        message = Message(mType=MessageType.read_file, mPayload=self._filename)
        self.send_message(message)

        response = self.recv_message()

        if response.payload == True:
            #prepare to receive from server
            print("Read file from server...")
        else:
            print("!! Server rejected file write")
                          
    def write(self):
        """ attempts to write a file to server """
        print("Write!")
        message = Message(mType=MessageType.write_file, mPayload=self._filename)
        self.send_message(message)
        
        response = self.recv_message()

        if response.payload == True:
            with open(self._filename) as fd:
                intxt = fd.read(1024)
                while intxt != "":
                    message = Message(mType=MessageType.write_file, mPayload=intxt)
                    self.send_message(message)
                    response = self.recv_message()
                    if response.payload == False:
                        break

                    intxt = fd.read(1024)

            message = Message(mType=MessageType.eof, mPayload=True)
            self.send_message(message)
            response = self.recv_message(message)
            
            if response.payload == True:
                print("!! Finished writing {0} to server".format(self._filename))
            else:
                print("!! Server indicated an error in writing file")
        else:
            print("!! Server rejected write command")

    def send_message(self, message):
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

    def recv_message(self):
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
                                
    def gen_nonce(self):
        """ generates a nonce to synchronize with the server """
        return os.urandom(16)                   
                  
    @staticmethod
    def three_dots(message):
        """ prints 3 dots with a .5 second delay between each dot """
        print(message, end='')
        sys.stdout.flush()
        
        for i in range(0,3):
            print('.', end='')
            sys.stdout.flush()
            time.sleep(0.5)

        print()


    def clear_screen(self):
        """ clears the console based on the operating system """
        os_sys = platform.system()

        print("clear screen")
        if os_sys == "Linux":
            os.system('clear')
        else:
            os.system('cls')
    
    def __del__(self):
        """destructor for chat client"""
        try:
            self._socket.close()
        except:
            print("Error closing socket")
        finally:
            self.three_dots("Exitting")
            

class IPFormatError(Exception):
    """custom exception to indicate an IP format error"""
    
    def __init__(self, value):
        self._message = value

    def __str__(self):
        return repr(self._message)


    
