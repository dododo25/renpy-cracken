import loader
import os
import pickle

from parser.block import Element
from parser.sl_default_parser import parse
from renpy.ast import Init, Screen
from renpy.sl2.slast import SLDefault

def test_parse_sl_default_statement():
    """
    screen test:
        default target = False <- this is our target block
    """
    expected = Element(type='default', value='default target = False')

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_sl_default_parser.rpyc')))[1]

    assert type(decompressed[0]) == Init
    assert type(decompressed[0].block[0]) == Screen
    assert type(decompressed[0].block[0].screen.children[0]) == SLDefault
    assert expected == parse(decompressed[0].block[0].screen.children[0])
