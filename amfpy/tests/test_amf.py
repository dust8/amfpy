import unittest
from amfpy.amf import *


class TestAMF(unittest.TestCase):

    def test_packet(self):
        data = b'\x00\x00\x00\x00\x00\x01\x00\x1bzh.fleetService.getFleetRow\x00\x03/79\x00\x00\x00\x13\n\x00\x00\x00\x03\x02\x00\x015\x02\x00\x03845\x02\x00\x015'
        amfdecoder = AMFDecoder()
        print(amfdecoder.decode(data))


if __name__ == '__main__':
    unittest.main()
