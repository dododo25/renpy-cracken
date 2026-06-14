import loader
import os
import pickle

from renpy.ast import Init, Screen
from renpy.sl2.slast import SLPass

def test_parse_sl_if_statement():
    """
    screen test:
        pass <- this is our target block
    """

    expected = 'pass'

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_sl_pass_parser.rpyc')))[1]

    assert type(decompressed[0]) == Init
    assert type(decompressed[0].block[0]) == Screen
    assert type(decompressed[0].block[0].screen.nchildren[0]) == SLPass
    assert expected == str(decompressed[0].block[0].screen.nchildren[0])
