import hashlib
import os
import pickle
import re
import socket
import threading
import time
import sys

from datetime import datetime

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
        print(self.time_message("--------------------------------------"))
        print (self.time_message("Listening @ {0} on port {1}".format(ip, self._port)))
        print (self.time_message("Using secret key: {0}".format(self._key)))
        print(self.time_message("--------------------------------------"))
        if re.match("127.0.*", ip):
            print(self.time_message("If this number is 127.0.0.1 or similar, comment out"))
            print(self.time_message("{0}\t{1}".format(ip, socket.getfqdn())))
            print(self.time_message("In /etc/hosts"))

        try:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            # 0.0.0.0 binds to all available interfaces
            self._socket.bind(("0.0.0.0", self._port))

            self._listen()
        except socket.error as ex:
            print(self.time_message("Error initializing socket: {0}".format(type(ex).__name__)))
            
    def _listen(self):
        """Listen for a client"""

        while True:
            self._socket.listen(5);
            (client, address) = self._socket.accept()
            clientThread = threading.Thread(target=self._worker, args=((client, address),))
            clientThread.start()
            
    def time_message(self, message):
        return datetime.now().strftime("!! %H:%M:%S: ") + message
            
    def _worker(self, args):
        """Handle a client"""
        (client, address) = args
        print(self.time_message("Client connected: {0}".format(address[0])))
        
        try:
            socket = self.shakehand(client)
            
            if socket:
                print(self.time_message("--------------------------------------"))
                message = socket.recv_message(decrypt=True)
                self.type_switch(message, socket)                                
        except (EOFError) as e:
            pass
        except:
            print(self.time_message("Client disconnected: {0}".format(address[0])))
            
        print(self.time_message("Exitting worker"))
    
    def type_switch(self, msg, client):
        if msg.type == MessageType.write_file:
            self.client_write(client, msg.payload)
        elif msg.type == MessageType.read_file:
            self.client_read(client, msg.payload)
        elif msg.type == MessageType.confirmation:
            pass

    def client_read(self, client, filename):
        """ handles a client attempting to read from the server  """
        print(self.time_message("Client requesting filename: {0}".format(filename)))

        try:
            with open(filename, 'rb') as fd:
                self.ack_client(client, True)
                intxt = fd.read(1024)
                while intxt != b'':
                    message = Message(mType=MessageType.write_file, mPayload=intxt)
                    client.send_message(message, encrypt=True)
                    intxt = fd.read(1024)

            message = Message(mType=MessageType.eof, mPayload=True)
            client.send_message(message, encrypt=True)
        except Exception as ex:
            self.send_error(client, "Error writing file: {0}".format(sys.exc_info()[1]))

    def client_write(self, client, filename):
        """ handles a client attempting to write to server """
        print(self.time_message("Client requested to write filename: {0}".format(filename)))

        try:
            md5_check = hashlib.md5()
            with open(filename, 'wb') as fd:
                self.ack_client(client, True)

                message = client.recv_message(decrypt=True)
                while message.type != MessageType.eof:
                    md5_check.update(message.payload)
                    fd.write(message.payload)
                    message = client.recv_message(decrypt=True)

                if message.payload != md5_check.digest():
                    print(self.time_message("File transfer rejected. Checksum mismatch. Expected: {0} Received: {1}".format(message.payload, md5_check.digest())))
                    response = Message(mType=MessageType.error, payload="Checksum on file did not match.")
                    client.send_message(response, encrypt=True)
                else:
                    print(self.time_message("File confirmed, checksum: {0}".format(md5_check.digest())))
                    self.ack_client(client, True)
                    print(self.time_message("Wrote {0} to file.".format(filename)))
        except Exception as ex:
            self.send_error(client, "Error writing file: {0}".format(sys.exc_info()[1]))

    def send_error(self, client, error):
        """ send error to client """
        self.eprint(self.time_message(error))
        error = Message(mType=MessageType.error, mPayload=error)

        client.send_message(error, encrypt=True)

    def shakehand(self, client):
        """ receives a handshake from the client containing cipher and iv """
        socket = SecureSocket(client, None, self._key, None)
        message = socket.recv_message(decrypt=False)
        try:
            if message.cipher != "aes256" and message.cipher != "aes128" and message.cipher != "none":
                self.ack_client(socket, False)
                socket = None
            else:
                socket.set_cipher(message.cipher)
                print(self.time_message("Cipher: {0}".format(message.cipher)))
                socket.set_iv(message.payload)
                socket.init_aescs()

                if message.cipher != "none":
                    print(self.time_message("Sending challenge."))
                    challenge = os.urandom(32)
                    socket.send_raw(challenge, encrypt=True)
                    response = socket.recv_raw(48, decrypt=True)
                    if int.from_bytes(challenge, "big") + 1 != int.from_bytes(response, "big"):
                        print(self.time_message("Client supplied bad response to challenge. Ending communication."))
                        time.sleep(1)
                        socket.close()
                        socket = None
                    else:
                        self.ack_client(socket, True)
                        #response_message = Message(mType=MessageType.confirmation, mPayload=True)
                        #socket.send_message(response_message, encrypt=True)
                else:
                    self.ack_client(socket, True)
                    
        except:
            print(self.time_message("Client could not decrypt challenge. Ending communication."))
            socket = None
            
        return socket

    def eprint(self, *args, **kwargs):
        print(*args, file=sys.stderr, **kwargs)
        
                
    def ack_client(self, client, ack):
        """ 
        ack_generates a confirmation message for the client with specified ack
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
            print(self.time_message("Error closing socket. May not have been initialized"))
        finally:
            print(self.time_message("Server exitting."))
