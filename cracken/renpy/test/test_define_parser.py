import loader
import os
import pickle

from renpy.ast import Init, Define

def test_parse_define_statement():
    """
    define value = 1 <- this is our target block
    """
    expected = 'define value = 1'

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_define_parser.rpyc')))[1]

    assert type(decompressed[0]) == Init
    assert type(decompressed[0].block[0]) == Define
    assert expected == str(decompressed[0].block[0])
