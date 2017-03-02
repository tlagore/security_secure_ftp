from getpass import getpass
import os
import pickle
import platform
import socket
import sys
import threading
import time
import struct

from secure_socket import Message, MessageType, SecureSocket

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
        self._iv = self.gen_nonce()
        self._cipher = cipher

        
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        self._socket = SecureSocket(sock, cipher, key, self._iv)        
        self.worker()

        time.sleep(3)

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
        self._socket.send_message(message, False)
        response = self._socket.recv_message(True)
        return response

    def read(self):
        """ reads a file from the server"""
        print("Read!")
        message = Message(mType=MessageType.read_file, mPayload=self._filename)
        self._socket.send_message(message, encrypt=True)

        response = self._socket.recv_message(decrypt=True)

        if response.payload == True:
            #prepare to receive from server
            print("Read file from server...")
        else:
            print("!! Server rejected file write")
                          
    def write(self):
        """ attempts to write a file to server """
        print("Write!")
        message = Message(mType=MessageType.write_file, mPayload=self._filename)
        self._socket.send_message(message, encrypt=True)
        
        response = self._socket.recv_message(decrypt=True)

        if response.payload == True:
            with open(self._filename) as fd:
                intxt = fd.read(1024)
                while intxt != "":
                    message = Message(mType=MessageType.write_file, mPayload=intxt)
                    self._socket.send_message(message, encrypt=True)
                    intxt = fd.read(1024)
                    
            message = Message(mType=MessageType.eof, mPayload=True)
            self._socket.send_message(message, encrypt=True)
            response = self._socket.recv_message(decrypt=True)
            
            if response.payload == True:
                print("!! Finished writing {0} to server".format(self._filename))
            else:
                print("!! Server indicated an error in writing file")
        else:
            print("!! Server rejected write command")
            
                                
    def gen_nonce(self):
        """ generates a nonce to synchronize with the server """
        return os.urandom(16)                   

    def eprint(self, *args, **kwargs):
        print(*args, file=sys.stderr, **kwargs)

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


    
