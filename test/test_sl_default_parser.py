import loader
import os
import pickle

from renpy.ast import Init, Screen
from renpy.sl2.slast import SLDefault

def test_parse_sl_default_statement():
    """
    screen test:
        default target = False <- this is our target block
    """
    expected = 'default target = False'

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_sl_default_parser.rpyc')))[1]

    assert type(decompressed[0]) == Init
    assert type(decompressed[0].block[0]) == Screen
    assert type(decompressed[0].block[0].screen.nchildren[0]) == SLDefault
    assert expected == str(decompressed[0].block[0].screen.nchildren[0])
