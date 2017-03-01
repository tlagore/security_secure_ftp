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

        self.handshake()

        message = Message(mType=MessageType.write_file, mPayload="helloworldhello! More things! Yeah! Love stuff.")
        self.send_message(message)

        #self._worker = threading.Thread(target=self.worker)
        #self._worker.start()
        #self._worker.join()

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

    def send_message(self, message):
        """ breaks message into 16 byte chunks and sends them decrypted """
        messageBytes = pickle.dumps(message)

        ## let's decide later if we want to send a fixed length header.
        ## if so, we need to figure out how python can do that
        self._socket.send(self.encrypt(str(len(messageBytes)).encode('UTF-8')))

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


    def recv_message(self, client):
        """ receives a message length then reads in a message and decrypts them """
        messageBytes = bytes([])
        chunk = self._socket.recv(16)
        messageSize = int(chunk.decode())
        print("got first chunk, size will be {0} bytes".format(int(chunk.decode())))
        
        while len(messageBytes) != messageSize:
            ## REMEMBER TO DECRYPT THE CHUNK HERE AFTER 16 BYTES READ ##
            chunk = self._socket.recv(1)
            messageBytes += chunk

        message = pickle.loads(messageBytes)
        print(message.payload)
        return message

    def handshake(self):
        """ generates an initialization vector for the server waits for confirmation """
        message = Message(mType=MessageType.handshake, mPayload=self._iv, mCipher=self._cipher)
        self._socket.send(pickle.dumps(message))
        response = pickle.loads(self.decrypt(self._socket.recv(2048)))
        print(response.payload)
        return response

    def read(self):
        """ reads a file from the server"""
        #message = Message(mType=MessageType.get_file, mPayload=self._filename)
        print("Read!")
                          
    def write(self):
        print("Write!")
        message = Message(mType=MessageType.write_file, mPayload=self._filename)
        self._socket.send(pickle.dumps(message))
        
        #response = Message(mType=MessageType.confirmation, mPayload=True)
        response = pickle.loads(self._socket.recv(2048))

        if response.payload == True:
            with open("test.txt") as fd:
                intxt = fd.read(16)
                while intxt != "":
                    message = Message(mType=MessageType.write_file, mPayload=intxt.encode())
                    self._socket.send(pickle.dumps(message))
                    response = pickle.loads(self._socket.recv(2048))
                    if response.payload == False:
                        break

                    intxt = fd.read(16)

            message = Message(mType=MessageType.eof, mPayload=True)
            self._socket.send(pickle.dumps(message))
            response = pickle.loads(self._socket.recv(2048))
            if response.payload == True:
                print("!! Finished writing {0} to server".format(self._filename))
            else:
                print("!! Server indicated an error in writing file")
        else:
            print("!! Server rejected write command")


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
                  
    def serialize_message(m_type=None, m_payload=None, m_target=None):
        """ creates a message object and returns the pickled (serialized) version of the object """

        ### Haven't used this yet, but might be useful to create message and serialize in same call ###
        message = Message(mType=m_type, mPayload=m_payload, target=m_target)
        return pickle.dumps(message)

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


    
