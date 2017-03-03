import base64
from Crypto.Cipher import AES

class AESCipher:
    def __init__(self, key, iv):
        self._bs = 16
        self._key = key
        self._iv = iv
        
    def init_suites(self):
        if self._key and self._iv:
            self._ecs = AES.new(self._key, AES.MODE_CBC, self._iv)
            self._dcs = AES.new(self._key, AES.MODE_CBC, self._iv)
    
    def encrypt(self, plain_text):
        print("---------------------------")
        
        print("raw:")
        print(len(plain_text))
        print(plain_text)

        b64_plain_text = base64.b64encode(plain_text)
        print("raw after base64 encoding")
        print(len(b64_plain_text))
        print(b64_plain_text)
                
        p_plain_text = self._pad(b64_plain_text)
        print("Padded b64 raw:")
        print(len(p_plain_text))
        print(p_plain_text)
        
        print("Cipher text:")
        ct = self._ecs.encrypt(p_plain_text)
        print(len(ct))
        print(ct)

        print("---------------------------")        

        return ct

    def decrypt(self, cipher_text):
        print("DECRYPTION")

        dct = self._dcs.decrypt(cipher_text)
        upt = self._unpad(dct)
        rb64t = base64.b64decode(upt)
        print("Decrypted")

        print("dct")
        print(len(dct))
        print(dct)

        print("upt")
        print(len(upt))
        print(upt)

        print("rb64t")
        print(len(rb64t))
        print(rb64t)
        
        print("DONE DECRYPTION")
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

    def set_iv(self, iv):
        self._iv = iv
