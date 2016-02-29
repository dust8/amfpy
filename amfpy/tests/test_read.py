import unittest
from amfpy.read import *


class TestAMF(unittest.TestCase):

    def test_object(self):
        data = b'\x03\x00\x04name\x02\x00\x04Mike\x00\x03age\x00@>\x00\x00\x00\x00\x00\x00\x00\x05alias\x02\x00\x04Mike\x00\x00\t'
        amfreader = AMFReader(data)
        self.assertEqual(read_value_type(amfreader),
                         {'name': 'Mike', 'alias': 'Mike', 'age': 30.0})

    def test_array(self):
        data = b'\x03\x00\x04name\x02\x00\x04Mike\x00\x03age\x00@>\x00\x00\x00\x00\x00\x00\x00\x05alias\x02\x00\x04Mike\x00\x00\t'
        amfreader = AMFReader(data)
        self.assertEqual(read_value_type(amfreader),
                         {'name': 'Mike', 'alias': 'Mike', 'age': 30.0})


if __name__ == '__main__':
    unittest.main()
