from enum import Enum

class MessageError(Exception):
    def __init__(self, message):
        self._message = message

    def __str__(self):
        return repr(self._message)

class MessageType(Enum):
    handshake = 0
    get_file = 1
    send_file = 2
    confirmation = 3

class Message:
    def __init__(self, mType=None, mPayload=None, mCipher=None):
        if mType is None:
            raise MessageError("Object of type 'Message' must be assigned a type.")

        if mPayload is None:
            raise MessageError("Object of type 'Message' cannot have an empty payload.")
        
        self._type = mType
        self._cipher = mCipher
        self._payload = mPayload

    @property
    def type(self):
        return self._type

    @property
    def payload(self):
        return self._payload

    @property
    def cipher(self):
        return self._cipher
