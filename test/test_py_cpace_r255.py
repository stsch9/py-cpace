import unittest
from src.py_cpace_r255 import generator_string, calculate_generator

PRS = b'Password'
CI = '6f630b425f726573706f6e6465720b415f696e69746961746f72'
sid = '7e4b4791d6a8ef019b936c79fb7f2c57'
gen_str = '11435061636552697374726574746f3235350850617373776f726464000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001a6f630b425f726573706f6e6465720b415f696e69746961746f72107e4b4791d6a8ef019b936c79fb7f2c57'
generator = 'a6fc82c3b8968fbb2e06fee81ca858586dea50d248f0c7ca6a18b0902a30b36b'

class TestCpaceR255(unittest.TestCase):
    def test_generator(self):
        gs = generator_string(PRS, bytes.fromhex(CI), bytes.fromhex(sid))
        self.assertEqual(bytes.fromhex(gen_str), gs)

    def test_calculate_generator(self):
        g = calculate_generator(PRS, bytes.fromhex(CI), bytes.fromhex(sid))
        self.assertEqual(g, bytes.fromhex(generator))

if __name__ == '__main__':
    unittest.main()