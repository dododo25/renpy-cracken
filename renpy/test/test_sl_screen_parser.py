import loader
import os
import pickle

from renpy.ast import Init, Screen
from renpy.sl2.slast import SLScreen

def test_parse_sl_screen_statement_without_properties():
    """
    screen target(a, b=0, *args, **kwargs): <- this is our target block
        add "test.jpg"
    """
    expected = 'screen target(a, b=0, *args, **kwargs):'
    expected_children = ['add "test.jpg"', '']

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_sl_screen_parser_without_properties.rpyc')))[1]

    assert type(decompressed[0]) == Init
    assert type(decompressed[0].block[0]) == Screen
    assert type(decompressed[0].block[0].screen) == SLScreen
    assert expected == str(decompressed[0].block[0].screen)
    assert expected_children == list(map(str, decompressed[0].block[0].screen.nchildren))

def test_parse_sl_screen_statement_with_properties():
    """
    screen target: <- this is our target block
        modal True
        sensitive False
        tag menu
        zorder 1
        variant "test"
        layer "master"

        add "test.jpg"
    """
    expected = 'screen target:'
    expected_children = ['modal True', 'sensitive False', 'tag menu', 'zorder 1', 'variant "test"', 'layer "master"', '', 'add "test.jpg"', '']

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_sl_screen_parser_with_properties.rpyc')))[1]

    assert type(decompressed[0]) == Init
    assert type(decompressed[0].block[0]) == Screen
    assert type(decompressed[0].block[0].screen) == SLScreen
    assert expected == str(decompressed[0].block[0].screen)
    assert expected_children == list(map(str, decompressed[0].block[0].screen.nchildren))
