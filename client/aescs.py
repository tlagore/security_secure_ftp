class AESCipher:
    def __init__(self, cipher, key, iv):
        self._key = key
        self._cipher = cipher
        self._iv = iv

    def init_suites(self):
        if self._cipher and self._key and self._iv:
        if self._cipher == 1: # AES 128
            self.encryption_suite = AES.new(key, AES.MODE_CBC, iv)
            self.decryption_suite = AES.new(key, AES.MODE_CBC, iv)
        if self._cipher == 2: # AES 256
            self.encryption_suite = AES.new(key, AES.MODE_CBC, iv)
            self.decryption_suite = AES.new(key, AES.MODE_CBC, iv)
        else: # no encryption
            pass
    
    def encrypt(self, plain_text):
        self.encryption_suite.encrypt(plain_text)
    def decrypt(self, cipher_text):
        self.decryption_suite.decrypt(cipher_text)

    def set_cipher(self, cipher):
        self._cipher = cipher

    def set_key(self, key):
        self._key = key

    def set_iv(self, iv):
        self._iv = iv
