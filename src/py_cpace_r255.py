from symtable import Class

from pysodium import (crypto_hash_sha512, crypto_core_ristretto255_from_hash, crypto_core_ristretto255_scalar_random,
                      crypto_scalarmult_ristretto255, crypto_core_ristretto255_is_valid_point)

DSI = b'CPaceRistretto255'
s_in_bytes = 128
identity = '0000000000000000000000000000000000000000000000000000000000000000'

def prepend_len(data: bytes) -> bytes:
    """prepend LEB128 encoding of length"""
    length = len(data)
    length_encoded = b""
    while True:
        if length < 128:
            length_encoded += bytes([length])
        else:
            length_encoded += bytes([(length & 0x7f) + 0x80])
        length = int(length >> 7)
        if length == 0:
            break
    return length_encoded + data


def lv_cat(*args) -> bytes:
    result = b""
    for arg in args:
        result += prepend_len(arg)
    return result

def generator_string(PRS: bytes, CI: bytes, sid: bytes):
    len_zpad = max(0, s_in_bytes - 1 - len(prepend_len(PRS)) - len(prepend_len(DSI)))

    return lv_cat(DSI, PRS, (b'\x00' * len_zpad), CI, sid)

def calculate_generator(PRS: bytes ,CI: bytes, sid: bytes):
    gen_str = generator_string(PRS, CI, sid)
    return crypto_core_ristretto255_from_hash(crypto_hash_sha512(gen_str))

# https://doc.libsodium.org/advanced/point-arithmetic/ristretto#scalar-multiplication
def scalar_mult_vfy(s: bytes, e: bytes) -> bytes:
    if crypto_core_ristretto255_is_valid_point(e):
        try:
            r = crypto_scalarmult_ristretto255(s,e)
            return r
        except ValueError:
            raise ValueError("No valid result")
    else:
        raise ValueError('No valid group element')

class CPace(object):
    def __init__(self, PRF: bytes, ADab = b'', CI = b'', sid = b''):
        self._prf = PRF
        self.ADab = ADab
        self.CI = CI
        self.sid = sid
        self._g = b''

    def compute_Ya(self):
        self._g = calculate_generator(self._prf, self.CI, self.sid)
        ya = crypto_core_ristretto255_scalar_random()
        ya = bytes.fromhex('da3d23700a9e5699258aef94dc060dfda5ebb61f02a5ea77fad53f4ff0976d08')
        Ya = crypto_scalarmult_ristretto255(ya, self._g)

        return Ya, self.ADab

    def compute_Yb(self):
        self._g = calculate_generator(self._prf, self.CI, self.sid)
        yb = crypto_core_ristretto255_scalar_random()
        Yb = crypto_scalarmult_ristretto255(yb, self._g)



