import base64
from Crypto.Cipher import AES

class AESCipher:
    def __init__(self, key, iv):
        self._bs = 16
        self._key = key
        self._iv = iv
        self._ready = False
        if self._iv and self._key:
            self._ready = True
        
    def init_suites(self):
        print("init cipher suites: key = {0}, iv = {1}".format(self._key, self._iv))
        if self._key and self._iv:
            self._ecs = AES.new(self._key, AES.MODE_CBC, self._iv)
            self._dcs = AES.new(self._key, AES.MODE_CBC, self._iv)
    
    def encrypt(self, plain_text):
        ct = None
        
        if self._ready:
            b64_plain_text = base64.b64encode(plain_text)

            p_plain_text = self._pad(b64_plain_text)

            self._ecs = AES.new(self._key, AES.MODE_CBC, self._iv)
            ct = self._ecs.encrypt(p_plain_text)
        
        return ct

    def decrypt(self, cipher_text):
        rb64t = None

        if self._ready:
            self._dcs = AES.new(self._key, AES.MODE_CBC, self._iv)
            dct = self._dcs.decrypt(cipher_text)
            
            upt = self._unpad(dct)
            
            rb64t = base64.b64decode(upt)
        
        return rb64t

    def _pad(self, s):
        length = 16 - (len(s) % 16)
        s += bytes([length])*length
        return s

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]

    def set_key(self, key):
        self._key = key
        if self._key and self._iv:
            self._ready = True

    def set_iv(self, iv):
        self._iv = iv
        if self._key and self._iv:
            self._ready = True
