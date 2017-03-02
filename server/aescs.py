from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

class AESCipher:
    def __init__(self, key, iv):
        self._backend = default_backend()
        self._key = key
        self._iv = iv
        
    def init_suites(self):
        if self._key and self._iv:
            self._cipher_suite = Cipher(algorithms.AES(bytes(self._key)), modes.CBC(self._iv), backend=self._backend) 
            self._encryptor = self._cipher_suite.encryptor()
            self._decryptor = self._cipher_suite.decryptor()
    
    def encrypt(self, plain_text):
        ct = _encryptor.update(plain_text)
        print(len(plain_text))
        print(len(ct))
        return ct

    def decrypt(self, cipher_text):
        pt = _decryptor.update(cipher_text)
        return pt

    def set_key(self, key):
        self._key = key

    def set_iv(self, iv):
        self._iv = iv
