import json
import hashlib
import pickle
import random
import re
import socket
import threading
import time
import traceback
import sys

from multiprocessing.connection import Listener
from secure_socket import Message, MessageType, SecureSocket

class FTPServer:
    """Chat server class to handle chat server interactions"""
    # continue
    def __init__(self, *args):
        """Constructor"""
        self._port = args[0]
        if len(args) == 2:
            self._key = args[1]
        self._socket = 0

    def start_server(self):
        """Initializes the server socket"""
        ip = socket.gethostbyname(socket.getfqdn())
        print ("Listening @ {0} on port {1}".format(ip, self._port))
        print ("Using secret key: {0}".format(self._key))
        
        if re.match("127.0.*", ip):
            print("If this number is 127.0.0.1 or similar, comment out")
            print("{0}\t{1}".format(ip, socket.getfqdn()))
            print("In /etc/hosts")

        try:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            # 0.0.0.0 binds to all available interfaces
            self._socket.bind(("0.0.0.0", self._port))

            self._listen()
        except socket.error as ex:
            print("Error initializing socket: {0}".format(type(ex).__name__))
            
    def _listen(self):
        """Listen for a client"""
        while True:
            self._socket.listen(5);
            (client, address) = self._socket.accept()
            print("Client connected.")
            clientThread = threading.Thread(target=self._worker, args=((client, address),))
            clientThread.start()            
    
    def _worker(self, args):
        """Handle a client"""
        (client, address) = args
        print("!! client connected {0}".format(address))
        
        try:
            socket = self.shakehand(client)
            
            if socket:
                message = socket.recv_message(decrypt=True)
                self.type_switch(message, socket)
                                
            else:
                print("!! Received bad client handshake")
            #self.recv_message(client)
                #message = pickle.loads(client.recv(2048))
                
            #message = pickle.loads(client.recv(2048))

        except (EOFError) as e:
            pass
        except:
            print("{0}".format(traceback.format_exception(sys.exc_info())))
            print("!! Client disconnected")
            
        print("!! Exitting worker")
    
    def type_switch(self, msg, client):
        print ("Message Details:")
        print ("type: {0}".format(msg.type))
        print ("cipher: {0}".format(msg.cipher))
        print ("payload: {0}".format(str(msg.payload)))

        if msg.type == MessageType.write_file:
            self.client_write(client, msg.payload)
        elif msg.type == MessageType.read_file:
            pass
        elif msg.type == MessageType.confirmation:
            pass

    def client_write(self, client, filename):
        """ handles a client attempting to write to server """
        print("filename: {0}".format(filename))

        try:
            with open(filename, 'wb') as fd:
                self.ack_client(client, True)

                message = client.recv_message(decrypt=True)
                while message.type != MessageType.eof:
                    fd.write(message.payload)
                    message = client.recv_message(decrypt=True)

                    self.ack_client(client, True)
        except Exception as ex:
            eprint("!! Error writing file: {0}".format(sys.exc_info()[1]))
            error = Message(mType=MessageType.error, mPayload="Error writing file: {0}: ".format(sys.exc_info()[1]))
            client.send_message(error, encrypt=True)            

    def shakehand(self, client):
        """ receives a handshake from the client containing cipher and iv """
        socket = SecureSocket(client, None, self._key, None)
        message = socket.recv_message(decrypt=False)

        if message.cipher != "aes256" and message.cipher != "aes128" and message.cipher != "none":
            self.ack_client(socket, False)
            socket = None
        else:
            self._cipher = message.cipher
            self._iv = message.payload
            socket.set_cipher(self._cipher)
            socket.set_iv(self._iv)
            self.ack_client(socket, True)
        return socket

    def eprint(self, *args, **kwargs):
        print(*args, file=sys.stderr, **kwargs)
        
    def read_message(self, message):
        """Read message from client"""
        return

    def encrypt(self, data):
        """ encrypts data and returns it """
        return data

    def decrypt(self, data):
        """ decrypts data and returns it """
        return data
                
    def ack_client(self, client, ack):
        """ 
        ack_client generates a confirmation message for the client with specified ack
        and sends the response to the client.

        ack is expected to be a boolean value (True/False)
        """
        response = Message(mType=MessageType.confirmation, mPayload=ack)
        client.send_message(response, encrypt=True)

    def __del__(self):
        """ destructor for chat server """        
        try:
            # if we want any persistence between sessions, write to file here.
            #with open('u.txt', 'w') as out:
                #json.dump(self._users, out)
            self._socket.close()
        except:
            print("Error closing socket. May not have been initialized")
        finally:
            print("Server exitting.")
