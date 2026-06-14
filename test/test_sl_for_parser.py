import loader
import os
import pickle

from renpy.ast import Init, Screen
from renpy.sl2.slast import SLFor

def test_parse_sl_if_statement():
    """
    screen test:
        for i in range(5): <- this is our target block
            add "sad.jpg"
    """
    expected = 'for i in range(5):'
    expected_children = ['add "sad.jpg"', '']

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_sl_for_parser.rpyc')))[1]

    assert type(decompressed[0]) == Init
    assert type(decompressed[0].block[0]) == Screen
    assert type(decompressed[0].block[0].screen.nchildren[0]) == SLFor
    assert expected == str(decompressed[0].block[0].screen.nchildren[0])
    assert expected_children == list(map(str, decompressed[0].block[0].screen.nchildren[0].nchildren))
