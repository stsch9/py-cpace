from symtable import Class
from typing import Literal
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

def lexiographically_larger(bytes1: bytes, bytes2: bytes) -> bool:
    "Returns True if bytes1>bytes2 using lexiographical ordering."
    min_len = min(len(bytes1), len(bytes2))
    for m in range(min_len):
        if bytes1[m] > bytes2[m]:
            return True
        elif bytes1[m] < bytes2[m]:
            return False
    return len(bytes1) > len(bytes2)

def o_cat(bytes1: bytes, bytes2: bytes) -> bytes:
    if lexiographically_larger(bytes1, bytes2):
        return b"oc" + bytes1 + bytes2
    else:
        return b"oc" + bytes2 + bytes1

def transcript_oc(Ya: bytes, ADa: bytes,Yb: bytes, ADb: bytes) -> bytes:
    result = o_cat(lv_cat(Ya, ADa),lv_cat(Yb, ADb))
    return result

def transcript_ir(Ya: bytes, ADa: bytes, Yb: bytes, ADb: bytes) -> bytes:
    result = lv_cat(Ya, ADa) + lv_cat(Yb, ADb)
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
    def __init__(self, PRF: bytes, mo: Literal['oc', 'ir'], ADa = b'', ADb = b'', CI = b'', sid = b''):
        self._prf = PRF
        self.ADa = ADa
        self.ADb = ADb
        self.CI = CI
        self.sid = sid
        self._g = b''
        if mo == 'oc':
            self.transcript = transcript_oc
        elif mo == 'ir':
            self.transcript = transcript_ir
        else:
            raise ValueError('Invalid Input')

    def compute_Ya(self):
        self._g = calculate_generator(self._prf, self.CI, self.sid)
        ya = crypto_core_ristretto255_scalar_random()
        ya = bytes.fromhex('da3d23700a9e5699258aef94dc060dfda5ebb61f02a5ea77fad53f4ff0976d08')
        Ya = crypto_scalarmult_ristretto255(ya, self._g)

        return Ya, self.ADa

    def compute_Yb(self, Ya: bytes):
        self._g = calculate_generator(self._prf, self.CI, self.sid)
        yb = crypto_core_ristretto255_scalar_random()
        Yb = crypto_scalarmult_ristretto255(yb, self._g)

        K = scalar_mult_vfy(yb, Ya)

        ISK = crypto_hash_sha512(lv_cat(DSI + b"_ISK", self.sid, K) + self.transcript(Ya, self.ADa, Yb, self.ADb))
