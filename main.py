import os
import struct
import sys
import re
import zlib

DEFAULT_BLOCK_SIZE = 12

def collect_files(filepath) -> list[str]:
    if os.path.isfile(filepath):
        if re.fullmatch(r'^.*\.rpyc$', filepath):
            return filepath, 

        return ()
    
    res = []

    for path in os.listdir(filepath):
        res += collect_files(os.path.join(filepath, path))

    return res

def decompress(filepath: str) -> bytes | None:
    with open(filepath, 'rb') as file:
        header = file.read(10)

        if not header == b'RENPY RPC2':
            return
        
        slot, start, length = None, None, None
        
        while not slot or slot > 1:
            slot, start, length = struct.unpack("III", file.read(DEFAULT_BLOCK_SIZE))

        if slot == 1:
            buf = bytearray(length)

            file.seek(start)
            file.readinto(buf)

            return zlib.decompress(buf)

        return None

def main(*argv):
    files = collect_files(os.path.abspath(argv[0]))

    if not len(files):
        print('No files to be found.')
        return

    for file in files:
        decompressed = decompress(file)

        with open(os.path.split(file)[-1].split('.')[0] + '-decompressed.txt', 'wb') as wfile:
            wfile.write(decompressed)

if __name__ == '__main__':
    main(*sys.argv[1:])