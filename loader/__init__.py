import pickle
import struct
import zlib

DEFAULT_BLOCK_SIZE = 12

ARCHIVE_HANDLERS = []

# This class was copied from RenPy v8.3.4
class RPAv1ArchiveHandler(object):
    """
    Archive handler handling RPAv1 archives.
    """

    archive_extension = ".rpa"

    @staticmethod
    def get_supported_extensions():
        return [".rpi"]

    @staticmethod
    def get_supported_headers():
        return [b"\x78\x9c"]

    @staticmethod
    def read_index(infile):
        return pickle.loads(zlib.decompress(infile.read()))

# This class was copied from RenPy v8.3.4
class RPAv2ArchiveHandler(object):
    """
    Archive handler handling RPAv2 archives.
    """

    archive_extension = ".rpa"

    @staticmethod
    def get_supported_extensions():
        return [".rpa"]

    @staticmethod
    def get_supported_headers():
        return [b"RPA-2.0 "]

    @staticmethod
    def read_index(infile):
        l = infile.read(24)
        offset = int(l[8:], 16)
        infile.seek(offset)
        return pickle.loads(zlib.decompress(infile.read()))

# This class was copied from RenPy v8.3.4
class RPAv3ArchiveHandler(object):
    """
    Archive handler handling RPAv3 archives.
    """

    archive_extension = ".rpa"

    @staticmethod
    def get_supported_extensions():
        return [".rpa"]

    @staticmethod
    def get_supported_headers():
        return [b"RPA-3.0 "]

    @staticmethod
    def read_index(infile):
        def start_to_bytes(s):
            if not s:
                return b''

            if not isinstance(s, bytes):
                s = s.encode("latin-1")

            return s

        l = infile.read(40)

        offset = int(l[8:24], 16)
        key    = int(l[25:33], 16)

        infile.seek(offset)
        index = pickle.loads(zlib.decompress(infile.read()))

        # Deobfuscate the index.
        for k in index.keys():
            if len(index[k][0]) == 2:
                index[k] = [(offset ^ key, dlen ^ key) for offset, dlen in index[k]]
            else:
                index[k] = [(offset ^ key, dlen ^ key, start_to_bytes(start)) for offset, dlen, start in index[k]]

        return index

ARCHIVE_HANDLERS.append(RPAv1ArchiveHandler)
ARCHIVE_HANDLERS.append(RPAv2ArchiveHandler)
ARCHIVE_HANDLERS.append(RPAv3ArchiveHandler)

MAX_HEADER_LENGTH = max(len(header) for handler in ARCHIVE_HANDLERS for header in handler.get_supported_headers())

def load_file(filepath: str):
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

            return zlib.decompress(buf)

        return None
    
def load_archive(filepath: str) -> tuple[dict | None, bool]:
    index = None

    with open(filepath, 'rb') as file:
        file_header = file.read(MAX_HEADER_LENGTH)

        for handler in ARCHIVE_HANDLERS:
            for header in handler.get_supported_headers():
                if file_header.startswith(header):
                    file.seek(0)
                    index = handler.read_index(file)
                    break

            if index:
                break

        if not index:
            return None, False

        res = {}

        for key, value in index.items():
            offset, length, _ = value[0]

            file.seek(offset)
            res[key] = file.read(length)

        return res, True

def is_file(filepath: str) -> bool:
    with open(filepath, 'rb') as file:
        return file.read(10) == b'RENPY RPC2'

    return False

def is_archive(filepath: str) -> bool:
    with open(filepath, 'rb') as file:
        file_header = file.read(MAX_HEADER_LENGTH)

        for handler in ARCHIVE_HANDLERS:
            for header in handler.get_supported_headers():
                if file_header.startswith(header):
                    file.seek(0)

                    try:
                        return handler.read_index(file) is not None
                    except UnicodeDecodeError:
                        return False

    return False
