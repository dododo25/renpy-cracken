import pickle
import struct
import zlib

DEFAULT_BLOCK_SIZE = 12

def decompress(filepath: str) -> bytes | None:
    with open(filepath, 'rb') as file:
        header = file.read(10)

        if header != b'RENPY RPC2':
            return

        slot, start, length = None, None, None

        while not slot or slot > 1:
            slot, start, length = struct.unpack("III", file.read(DEFAULT_BLOCK_SIZE))

        if slot == 1:
            buf = bytearray(length)

            file.seek(start)
            file.readinto(buf)

            return pickle.loads(zlib.decompress(buf))[1]

        return None
