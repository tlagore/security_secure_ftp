from Crypto.Cipher import AES


class AESCipher:
    def __init__(self, key, iv):
        self._bs = AES.block_size
        self._key = key
        self._iv = iv
        
    def init_suites(self):
        if self._key and self._iv:
            self._cs = AES.new(self._key, AES.MODE_CBC, self._iv)
    
    def encrypt(self, plain_text):
        print("Plain Text:")
        print(len(plain_text))
        print(plain_text)
        
        p_plain_text = self._pad(plain_text)
        print("Padded Plain Text:")
        print(len(p_plain_text))
        print(p_plain_text)
        
        print("Cipher Text:")
        ct = self._cs.encrypt(plain_text)
        print(len(ct))
        print(ct)

        print("Decrypted and unpadded Cipher Text:")
        pt = self._cs.decrypt(ct)
        upt = self._unpad(pt)
        print(len(upt))
        print(upt)
        
        return ct

    def decrypt(self, cipher_text):
        pt = self._cs.decrypt(cipher_text)
        upt = self._unpad(pt)
        print("Decrypt")
        print(len(cipher_text))
        print(len(upt))
        return upt

    def _pad(self, s):
        return s + ((self._bs - len(s) % self._bs) * chr(self._bs - len(s) % self._bs))

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]

    def set_key(self, key):
        self._key = key

    def set_iv(self, iv):
        self._iv = iv
