import unittest
from src.py_cpace_r255 import (generator_string, calculate_generator, CPace, scalar_mult_vfy, lexiographically_larger,
                               transcript_oc, o_cat, transcript_ir,scalar_mult_vfy)

PRS = b'Password'
CI = '6f630b425f726573706f6e6465720b415f696e69746961746f72'
sid = '7e4b4791d6a8ef019b936c79fb7f2c57'
gen_str = '11435061636552697374726574746f3235350850617373776f726464000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001a6f630b425f726573706f6e6465720b415f696e69746961746f72107e4b4791d6a8ef019b936c79fb7f2c57'
generator = 'a6fc82c3b8968fbb2e06fee81ca858586dea50d248f0c7ca6a18b0902a30b36b'
ADa = b'ADa'
ya = 'da3d23700a9e5699258aef94dc060dfda5ebb61f02a5ea77fad53f4ff0976d08'
Ya = 'd40fb265a7abeaee7939d91a585fe59f7053f982c296ec413c624c669308f87a'
ADb = b'ADb'
yb = 'd2316b454718c35362d83d69df6320f38578ed5984651435e2949762d900b80d'
Yb = '08bcf6e9777a9c313a3db6daa510f2d398403319c2341bd506a92e672eb7e307'

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
        cpace = CPace(PRS, mo='oc', ADa=ADa, ADb=b'', CI=bytes.fromhex(CI), sid=bytes.fromhex(sid))
        Ya_star, ADa_star = cpace.compute_Ya()
        self.assertEqual(Ya_star, bytes.fromhex(Ya))
        self.assertEqual(ADa_star, ADa)

    def test_scalar_mult_vfy(self):
        with self.assertRaises(ValueError):
            scalar_mult_vfy(bytes.fromhex(s), bytes.fromhex(Y_i1))
        with self.assertRaises(ValueError):
            scalar_mult_vfy(bytes.fromhex(s), bytes.fromhex(Y_i2))

    def test_lexiographically_larger(self):
        self.assertFalse(lexiographically_larger(b"\0", b"\0\0"))
        self.assertTrue(lexiographically_larger(b"\1", b"\0\0"))
        self.assertTrue(lexiographically_larger(b"\0\0", b"\0"))
        self.assertFalse(lexiographically_larger(b"\0\0", b"\1"))
        self.assertFalse(lexiographically_larger(b"\0\1", b"\1"))
        self.assertFalse(lexiographically_larger(b"ABCD", b"BCD"))

    def test_o_cat(self):
        self.assertEqual(o_cat(b"ABCD",b"BCD"), bytes.fromhex('6f6342434441424344'))
        self.assertEqual(o_cat(b"BCD",b"ABCDE"), bytes.fromhex('6f634243444142434445'))

    def test_transcript_oc(self):
        self.assertEqual(transcript_oc(b"123", b"PartyA", b"234",b"PartyB"), bytes.fromhex('6f6303323334065061727479420331323306506172747941'))
        self.assertEqual(transcript_oc(b"3456",b"PartyA",b"2345",b"PartyB"), bytes.fromhex('6f63043334353606506172747941043233343506506172747942'))

    def test_transcript_ir(self):
        self.assertEqual(transcript_ir(b"123", b"PartyA", b"234",b"PartyB"), bytes.fromhex('03313233065061727479410332333406506172747942'))
        self.assertEqual(transcript_ir(b"3456",b"PartyA",b"2345",b"PartyB"), bytes.fromhex('043334353606506172747941043233343506506172747942'))

    def test_K(self):
        self.assertEqual(scalar_mult_vfy(bytes.fromhex(ya),bytes.fromhex(Yb)), bytes.fromhex('e22b1ef7788f661478f3cddd4c600774fc0f41e6b711569190ff88fa0e607e09'))
        self.assertEqual(scalar_mult_vfy(bytes.fromhex(yb), bytes.fromhex(Ya)), bytes.fromhex('e22b1ef7788f661478f3cddd4c600774fc0f41e6b711569190ff88fa0e607e09'))

if __name__ == '__main__':
    unittest.main()