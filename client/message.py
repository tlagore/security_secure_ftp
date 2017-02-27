from enum import Enum

class MessageError(Exception):
    def __init__(self, message):
        self._message = message

    def __str__(self):
        return repr(self._message):

class MessageType(Enum):
    handshake = 0
    get_file = 1
    send_file = 2

class Message:
    def __init__(self, mType=None, mPayload=None):
        if mType is None:
            raise MessageError("Object of type 'Message' must be assigned a type.")

        if mPayload is None:
            raise MessageError("Object of type 'Message' cannot have an empty payload.")

        self._type = mType
        self._payload = mPayload


    @property
    def type(self):
        return self._type

    @property
    def payload(self):
        return self._payload
