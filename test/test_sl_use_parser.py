import loader
import os
import pickle

from renpy.ast import Init, Screen
from renpy.sl2.slast import SLUse

def test_parse_sl_use_statement():
    """
    screen test1(index):
        add "test.png"

    screen test2:
        use test1(0) id "id" <- this is our target block
    """
    expected = 'use test1(0) id "id"'

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_sl_use_parser.rpyc')))[1]

    assert type(decompressed[1]) == Init
    assert type(decompressed[1].block[0]) == Screen
    assert type(decompressed[1].block[0].screen.nchildren[0]) == SLUse
    assert expected == str(decompressed[1].block[0].screen.nchildren[0])

def test_parse_sl_use_with_expression_statement():
    """
    screen test1(index):
        add "test.png"

    screen test2:
        use expression member.screen pass (0) <- this is our target block
    """
    expected = 'use expression member.screen pass (0)'

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_sl_use_with_expression_parser.rpyc')))[1]

    assert type(decompressed[1]) == Init
    assert type(decompressed[1].block[0]) == Screen
    assert type(decompressed[1].block[0].screen.nchildren[0]) == SLUse
    assert expected == str(decompressed[1].block[0].screen.nchildren[0])
