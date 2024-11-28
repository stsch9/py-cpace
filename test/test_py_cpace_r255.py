import unittest
from src.py_cpace_r255 import generator_string, calculate_generator, CPace, scalar_mult_vfy
from pysodium import crypto_core_ristretto255_is_valid_point

PRS = b'Password'
CI = '6f630b425f726573706f6e6465720b415f696e69746961746f72'
sid = '7e4b4791d6a8ef019b936c79fb7f2c57'
gen_str = '11435061636552697374726574746f3235350850617373776f726464000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001a6f630b425f726573706f6e6465720b415f696e69746961746f72107e4b4791d6a8ef019b936c79fb7f2c57'
generator = 'a6fc82c3b8968fbb2e06fee81ca858586dea50d248f0c7ca6a18b0902a30b36b'
ADa = b'ADa'
ya = 'da3d23700a9e5699258aef94dc060dfda5ebb61f02a5ea77fad53f4ff0976d08'
Ya = 'd40fb265a7abeaee7939d91a585fe59f7053f982c296ec413c624c669308f87a'


s = '7cd0e075fa7955ba52c02759a6c90dbbfc10e6d40aea8d283e407d88cf538a05'
Y_i1 = '2b3c6b8c4f3800e7aef6864025b4ed79bd599117e427c41bd47d93d654b4a51c'
Y_i2 = '0000000000000000000000000000000000000000000000000000000000000000'

class TestCpaceR255(unittest.TestCase):
    def test_generator(self):
        gs = generator_string(PRS, bytes.fromhex(CI), bytes.fromhex(sid))
        self.assertEqual(bytes.fromhex(gen_str), gs)

    def test_calculate_generator(self):
        g = calculate_generator(PRS, bytes.fromhex(CI), bytes.fromhex(sid))
        self.assertEqual(g, bytes.fromhex(generator))

    def test_compute_Ya(self):
        cpace = CPace(PRS, ADa=ADa, CI=bytes.fromhex(CI), sid=bytes.fromhex(sid))
        Ya_star, ADa_star = cpace.compute_Ya()
        self.assertEqual(Ya_star, bytes.fromhex(Ya))
        self.assertEqual(ADa_star, ADa)

    def test_scalar_mult_vfy(self):
        with self.assertRaises(ValueError):
            scalar_mult_vfy(bytes.fromhex(s), bytes.fromhex(Y_i1))
        with self.assertRaises(ValueError):
            scalar_mult_vfy(bytes.fromhex(s), bytes.fromhex(Y_i2))

if __name__ == '__main__':
    unittest.main()