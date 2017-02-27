import json
import hashlib
import pickle
import random
import re
import socket
import threading
import traceback
import sys

from message import Message, MessageType

class FTPServer:
    """Chat server class to handle chat server interactions"""
    # continue
    def __init__(self, port):
        """ChatServer Constructor"""
        self._port = port
        self._socket = 0

    def start_server(self):
        """Initializes the server socket"""
        ip = socket.gethostbyname(socket.getfqdn())
        print("Starting server on port {0}".format(self._port))
        print("Please ensure port forwarding for {0} on port {1}".format(ip, self._port))

        if re.match("127.0.*", ip):
            print("If this number is 127.0.0.1 or similar, comment out")
            print("{0}\t{1}".format(ip, socket.getfqdn()))
            print("In /etc/hosts")

        try:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            # 0.0.0.0 binds to all available interfaces
            self._socket.bind(("0.0.0.0", self._port))
            #self._socket.bind(('127.0.0.1', self._port))
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

        print("Got a client!")
        #main worker loop, receive message and check contents
        '''
        try:
            message = pickle.loads(client.recv(2048))
            while message:
                if message._type == Message.MessageType.signup:
                    self.sign_up(message, client)
                if message._type == Message.MessageType.login:
                    self.login(message, client)
                if message._type == Message.MessageType.join_group:
                    self.join_group(message, client)
                    
                message = pickle.loads(client.recv(2048))
        except:
            print("{0}".format(traceback.format_exception(*sys.exc_info())))
            print("Client disconnected")
        '''
        
        print("Exitting worker")
        
    def ack_client(self, client, ack):
        """ 
        ack_client generates a confirmation message for the client with specified ack
        and sends the response to the client.

        ack is expected to be a boolean value (True/False)
        """
        
        response = Message(mType=MessageType.confirmation, mPayload=ack)
        client.send(pickle.dumps(response))            

    def __del__(self):
        """ destructor for chat server """        
        try:
            # if we want any persistence between sessions, write to file here.
            #with open('u.txt', 'w') as out:
            #    json.dump(self._users, out)
            self._socket.close()
        except:
            print("Error closing socket. May not have been initialized")
        finally:
            print("Server exitting.")
