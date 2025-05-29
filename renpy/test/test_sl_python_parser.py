import loader
import os
import pickle

from renpy.ast import Init, Screen
from renpy.sl2.slast import SLPython

def test_parse_sl_if_statement():
    """
    screen test:
        python: <- this is our target block
            value = 1
    """
    expected = 'python:'
    expected_children = ['\nvalue = 1\n']

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_sl_python_parser.rpyc')))[1]

    assert type(decompressed[0]) == Init
    assert type(decompressed[0].block[0]) == Screen
    assert type(decompressed[0].block[0].screen.nchildren[0]) == SLPython
    assert expected == str(decompressed[0].block[0].screen.nchildren[0])
    assert expected_children == list(map(str, decompressed[0].block[0].screen.nchildren[0].nchildren))
