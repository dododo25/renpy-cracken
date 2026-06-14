import loader
import os
import pickle

from renpy.ast import Init, Screen
from renpy.sl2.slast import SLIf

def test_parse_sl_if_statement():
    """
    screen test:
        imagemap:
            if a == 0: <- this is our target block
                add "sad.jpg"
            elif a == 1:
                auto "happy.jpg"
            else:
                add "exited.jpg"
    """
    expected_children = ['if a == 0:', 'elif a == 1:', 'else:', '']
    expected_children_children = [['add "sad.jpg"'], ['auto "happy.jpg"'], ['add "exited.jpg"'], None]

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_sl_if_parser.rpyc')))[1]

    assert type(decompressed[0]) == Init
    assert type(decompressed[0].block[0]) == Screen
    assert type(decompressed[0].block[0].screen.nchildren[0].nchildren[0]) == SLIf
    assert decompressed[0].block[0].screen.nchildren[0].nchildren[0].nexclude
    assert expected_children == list(map(str, decompressed[0].block[0].screen.nchildren[0].nchildren[0].nchildren))
    assert expected_children_children == list(map(lambda part: list(map(str, part.nchildren)) if part.nchildren else None, \
                                                  decompressed[0].block[0].screen.nchildren[0].nchildren[0].nchildren))
