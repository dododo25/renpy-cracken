import loader
import os
import pickle

from renpy.ast import Init, Screen
from renpy.sl2.slast import SLIf

def test_parse_sl_if_statement():
    """
    screen test:
        if a == 0: <- this is our target block
            add "sad.jpg"
        elif a == 1:
            add "happy.jpg"
        else:
            add "exited.jpg"
    """
    expected_children = ['if a == 0:', 'elif a == 1:', 'else:']

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_sl_if_parser.rpyc')))[1]

    assert type(decompressed[0]) == Init
    assert type(decompressed[0].block[0]) == Screen
    assert type(decompressed[0].block[0].screen.nchildren[0]) == SLIf
    assert decompressed[0].block[0].screen.nchildren[0].nexclude
    assert expected_children == list(map(str, decompressed[0].block[0].screen.nchildren[0].nchildren))
