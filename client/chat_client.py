from getpass import getpass
import os
import pickle
import platform
import socket
import sys
import threading
import time

from message import Message

class ChatClient:
    """Chat server class to handle chat server interactions"""

    def __init__(self, host, port):
        """constructor for chat client"""
        print("{0} {1}".format(host, port))

        self._user = None
        self._group = None

        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((host, port))

        self._listenServer = threading.Thread(target=self.listen_server)
        self._listenClient = threading.Thread(target=self.listen_client)
        
        self._listenServer.start()
        self._listenClient.start()

        self._listenServer.join()
        self._listenClient.join()

    def listen_server(self):
        """listens for interaction from the server"""
        #haven't had a use for this yet because usually the interaction is:
        #client sends a message -> server responds. Not much need to listen unless we've sent something
                    
    def listen_client(self):
        """listen for client input to pass to the server"""
        #do client stuff
        #ie: self._socket.send(pickle.dumps(object))
        #response = pickle.loads(self._socket.recv(2048))
        #do stuff with response

                  
    def serialize_message(m_type=None, m_payload=None, m_target=None):
        """ creates a message object and returns the pickled (serialized) version of the object """

        ### Haven't used this yet, but might be useful to create message and serialize in same call ###
        message = Message(mType=m_type, mPayload=m_payload, target=m_target)
        return pickle.dumps(message)
        
            
    def sign_up(self):
        """ 
        handles client side interaction of signing in to server
        
        checks with the server to ensure name is available
        """
        user = input("Please enter a user name (\"cancel\" to cancel): ")
        response = self.request_user(user)

        while response._payload != True and user != "cancel":
            print("User name is taken.")
            user = input("Please enter a user name (\"cancel\" to cancel): ")
            response = self.request_user(user)
        
        if user != "cancel":
            psw = getpass()
            psw2 = getpass(prompt="Repeat password: ")
            while psw != psw2:
                print("Passwords do not match")
                psw = getpass()
                psw2 = getpass(prompt="Repeat password: ")
                
            message = Message(mType=Message.MessageType.signup, mPayload=psw)
            self._socket.send(pickle.dumps(message))
            response = pickle.loads(self._socket.recv(2048))
        
            if response._payload:
                Menu.three_dots("Successfully signed up")
        else:
            Menu.three_dots("Cancelled signup process")
            
            
    def request_user(self, user):
        message = Message(mType=Message.MessageType.signup, mPayload=user)
        self._socket.send(pickle.dumps(message))
        response = pickle.loads(self._socket.recv(2048))
        return response
        
    def login(self):
        message = self.get_creds()
        self._socket.send(pickle.dumps(message))
        response = pickle.loads(self._socket.recv(2048))
        
        while response._payload != True:
            print("Invalid user or password.")
            message = self.get_creds()

            self._socket.send(pickle.dumps(message))
            response = pickle.loads(self._socket.recv(2048))
            
            if message._target == "cancel":
                break

        if message._target != "cancel":
            Menu.three_dots("Login successful")
            self._user = message._target
            self.user_loop()
            
        else:
            Menu.three_dots("Login cancelled")

    def get_creds(self):
        user = input("User name (\"cancel\" to abort): ")
        psw = getpass()
        message = Message(mType=Message.MessageType.login, target=user, mPayload=psw)
        return message
        
    def close(self):
        print("exit!")

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
            

class IPFormat(Exception):
    """custom exception to indicate an IP format error"""
    
    def __init__(self, value):
        self._message = value

    def __str__(self):
        return repr(self._message)


    
