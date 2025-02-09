import loader
import os
import pickle

from renpy.ast import Init, Default

def test_parse_default_statement():
    """
    default value = 1 <- this is our target block
    """
    expected = 'default value = 1'

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_default_parser.rpyc')))[1]

    assert type(decompressed[0]) == Init
    assert type(decompressed[0].block[0]) == Default
    assert expected == str(decompressed[0].block[0])
