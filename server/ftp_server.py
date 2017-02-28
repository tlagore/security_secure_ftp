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

        print("Got a client!")
        #main worker loop, receive message and check contents
        try:
            message = pickle.loads(client.recv(2048))
            self.msg_type(message.type)

#            self.read_message(message)

            self.ack_client(client, True)
            
        except:
            print("{0}".format(traceback.format_exception(sys.exc_info())))
            print("Client disconnected")
            
        print("Exitting worker")

    def msg_type(x):
        return {
            'handshake': self.shakehand(),
            'get_file': sys.exit(0),
            'send_file': sys.exit(0),
            'confirmation': sys.exit(0),
        }[x]

    def shakehand(self):
        print ("payload: {0}".format(str(message.payload)))
        print ("cipher: {0}".format(message.cipher))
                    
    def read_message(self, message):
        """Read message from client"""

        print ("message : {0}".format(args))
        if message.type:
            '''use encryption'''
            print ("Encrypting with {0}".format(args[2]))
        else:
            if len(args) == 2:
                '''no encryption'''
                print ("Not excrypting communications")
            else:
                '''too many or too few args'''
                print("Invalid number of args")
                return

        if args[0] == 'read':
            '''send file to client'''
            '''check if file exists'''
            print ("Server sends file {0}".format(args[1]))
        else:
            if args[0] == 'write':
                '''recv or update file from client'''
                print ("Server recieves file {0}".format(args[1]))
            else:
                print ("args[0] was an invalid command")
                return
        
                
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
                #json.dump(self._users, out)
            self._socket.close()
        except:
            print("Error closing socket. May not have been initialized")
        finally:
            print("Server exitting.")
