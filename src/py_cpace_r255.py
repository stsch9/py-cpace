from pysodium import crypto_hash_sha512, crypto_core_ristretto255_from_hash, crypto_core_ristretto255_scalar_random

DSI = b'CPaceRistretto255'
s_in_bytes = 128

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