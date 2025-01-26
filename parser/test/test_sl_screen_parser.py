import loader
import os
import pickle

from parser.block import Container, Element
from parser.sl_screen_parser import parse
from renpy.ast import Init, Screen
from renpy.sl2.slast import SLScreen

def test_parse_sl_screen_statement_without_properties():
    """
    screen target(a, b=0, *args, **kwargs): <- this is our target block
        add "test.jpg"
    """
    expected = Container(type='screen', value='screen target(a, b=0, *args, **kwargs):')

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_sl_screen_parser_without_properties.rpyc')))[1]

    assert type(decompressed[0]) == Init
    assert type(decompressed[0].block[0]) == Screen
    assert type(decompressed[0].block[0].screen) == SLScreen

    parsed = parse(decompressed[0].block[0].screen)

    assert expected.__class__ == parsed.__class__
    assert expected.value == parsed.value

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
    expected = Container(type='screen', value='screen target:', children=[Element(type='property', value='modal True'), Element(type='property', value='sensitive False'), Element(type='property', value='tag menu'), Element(type='property', value='zorder 1'), Element(type='property', value='variant "test"'), Element(type='property', value='layer "master"'), None])

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_sl_screen_parser_with_properties.rpyc')))[1]

    assert type(decompressed[0]) == Init
    assert type(decompressed[0].block[0]) == Screen
    assert type(decompressed[0].block[0].screen) == SLScreen

    parsed = parse(decompressed[0].block[0].screen)

    assert expected.__class__ == parsed.__class__
    assert expected.value == parsed.value

    for index, left, right in zip(range(len(expected.children)), expected.children, parsed.children):
        if index == len(expected.children) - 1:
            break

        assert left.value == right.value
