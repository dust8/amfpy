from amfpy.read import *


class AMF:

    def encode(self, input):
        '''Encodes the object input, and returns bytes.
        '''
        raise NotImplementedError

    def decode(self, input):
        '''Decodes the object input and return.
        '''
        raise NotImplementedError


class AMFDecoder(AMF):

    def __init__(self):
        self.reader = None

    def decode(self, input):
        self.reader = AMFReader(input)
        return decode_amf_packet(self.reader)
