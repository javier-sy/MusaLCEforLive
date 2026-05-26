"""Small utilities shared by the OSC-side handlers."""

import base64


def pack_bigint(i) -> bytearray:
    b = bytearray()
    while i:
        b.append(i & 0xFF)
        i >>= 8
    return b


def encode_ptr(ptr) -> str:
    return base64.standard_b64encode(pack_bigint(ptr))
