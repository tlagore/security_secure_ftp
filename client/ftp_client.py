import hashlib
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
        self.eprint("!! Client starting. Arguments: ".format(host, port))
        self.eprint("!! \thost: {0}".format(host))
        self.eprint("!! \tport: {0}".format(port))
        self.eprint("!! \tcommand: {0}".format(command))
        self.eprint("!! \tfilename: {0}".format(filename))
        self.eprint("!! \tcipher: {0}".format(cipher))
        self.eprint("!! \tkey: {0}".format(key))

        self._host = host
        self._port = port
        self._command = command
        self._filename = filename
        self._iv = self.gen_nonce()
        self._cipher = cipher
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        
        skey = self.stretch_key_c(cipher, key) #stretch the key

        self._socket = SecureSocket(sock, cipher, skey, self._iv)        
        self.worker()
        

    def worker(self):
        """ worker thread for ftp_client """
        response = self.handshake()
        
        if response.payload == True:
            if self._command == "read":
                self.read()
            elif self._command == "write":
                if sys.stdin.isatty():
                    print("!! Improper usage, pipe file data into program using 'cat file.ext | python3 __main__.py [args]'")
                else:
                    self.write()
        else:
            self.eprint("!! Server denied connection.")
            self.eprint("!! {0}".format(response.payload))
        
        
    def handshake(self):
        """ generates an initialization vector for the server waits for confirmation """
        try:
            message = Message(mType=MessageType.handshake, mPayload=self._iv, mCipher=self._cipher)
            self._socket.send_message(message, encrypt=False)

            if self._cipher != "none":
                ## Receive challenge, decrypt, add one, send back ##
                challenge = self._socket.recv_raw(32, decrypt=True)
                challenge = int.from_bytes(challenge, "big") + 1
                self._socket.send_raw(challenge.to_bytes(16, "big"), encrypt=True)
                ## Get server response ##
                response = self._socket.recv_message(decrypt=True)
                return response
            else:
                response = self._socket.recv_message(decrypt=True)
                return response
        except:
            return Message(mType=MessageType.error, mPayload = "Invalid Key.")
        

    def read(self):
        """ reads a file from the server"""
        message = Message(mType=MessageType.read_file, mPayload=self._filename)
        self._socket.send_message(message, encrypt=True)

        response = self._socket.recv_message(decrypt=True)

        if response.payload == True:
            self.eprint("!! Receiving file...")
            md5_check = hashlib.md5()
            response = self._socket.recv_message(decrypt=True)
            while response.type != MessageType.eof and response.type != MessageType.error:
                md5_check.update(response.payload)
                try:
                    print(response.payload.decode())
                except:
                    sys.stdout.buffer.write(response.payload)
                response = self._socket.recv_message(decrypt=True)

            if md5_check.digest() != response.payload:
                self.eprint("File transfer rejected. Checksum mismatch. Expected: {0} Received: {1}".format(response.payload, md5_check.digest()))
            else:
                digest = ''.join('{:02x}'.format(x) for x in md5_check.digest())
                self.eprint("!! File confirmed, checksum: {0}".format(digest))
                
        else:    
            self.eprint("!! Server rejected read command")

        if response.type == MessageType.error:
            self.eprint("!! {0}".format(response.payload))

                          
    def write(self):
        """ attempts to write a file to server """
        message = Message(mType=MessageType.write_file, mPayload=self._filename)
        self._socket.send_message(message, encrypt=True)
        
        response = self._socket.recv_message(decrypt=True)

        md5_check = hashlib.md5()
        if response.payload == True:
            self.eprint("!! Sending file...")
            intxt = sys.stdin.buffer.read(1024)
            while intxt != b'':
                md5_check.update(intxt)
                message = Message(mType=MessageType.write_file, mPayload=intxt)
                self._socket.send_message(message, encrypt=True)
                intxt = sys.stdin.buffer.read(1024)

            digest = ''.join('{:02x}'.format(x) for x in md5_check.digest())
            print("!! File sent, checksum: {0}".format(digest))

            message = Message(mType=MessageType.eof, mPayload=md5_check.digest())
            self._socket.send_message(message, encrypt=True)

            response = self._socket.recv_message(decrypt=True)
            
            if response.payload == True:
                self.eprint("!! Finished writing {0} to server".format(self._filename))
            else:
                self.eprint("!! Server indicated an error in writing file")
                self.eprint("!! {0}".format(response.payload))
        else:
            if response.type == MessageType.error:
                self.eprint("!! {0}".format(response.payload))
                
            self.eprint("!! Server rejected write command")
                                
    def gen_nonce(self):
        """ generates a nonce to synchronize with the server """
        return os.urandom(16)

    def eprint(self, *args, **kwargs):
        print(*args, file=sys.stderr, **kwargs)

    def stretch_key_c(self, cipher, key):
        if cipher == 'aes256':
            fill = 32
        elif cipher == 'aes128':
            fill = 16
        else:
            return key # nothing to change

        orig_key = key
        length = len(key)
        stretch = fill - length
        if stretch > 0:
            mod = stretch % length
            div = int(stretch / length)
            for x in range(0,div):
                key += orig_key
            key += key[:(mod)]
        return key

    def clear_screen(self):
        """ clears the console based on the operating system """
        os_sys = platform.system()

        self.eprint("clear screen")
        if os_sys == "Linux":
            os.system('clear')
        else:
            os.system('cls')
    
    def __del__(self):
        """destructor for chat client"""
        try:
            self._socket.close()
        except:
            self.eprint("Error closing socket")     

class IPFormatError(Exception):
    """custom exception to indicate an IP format error"""
    
    def __init__(self, value):
        self._message = value

    def __str__(self):
        return repr(self._message)


    
