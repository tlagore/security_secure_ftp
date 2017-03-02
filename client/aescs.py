from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

class AESCipher:
    def __init__(self, key, iv):
        self._backend = default_backend()
        self._key = key
        self._iv = iv
        
    def init_suites(self):
        if self._key and self._iv:
            self._cs = Cipher(algorithms.AES(bytes(self._key, 'utf-8')), modes.CBC(self._iv), backend=self._backend) 
            self._encryptor = self._cs.encryptor()
            self._decryptor = self._cs.decryptor()
    
    def encrypt(self, plain_text):
        print(len(plain_text))
        print(plain_text)
        padder = padding.PKCS7(128).padder()

        plain_text = padder.update(plain_text)
        plain_text += padder.finalize()
        print("Encrypt")
        ct = self._encryptor.update(plain_text)
        print(len(ct))
        print(ct)
        print("Decrypt")
        pt = self._decryptor.update(ct)
        print(len(ct))
        print(len(pt))
        print(pt)
        return ct

    def decrypt(self, cipher_text):
        pt = self._decryptor.update(cipher_text)
        print("Decrypt")
        print(len(cipher_text))
        print(len(pt))
        return pt

    def set_key(self, key):
        self._key = key

    def set_iv(self, iv):
        self._iv = iv
