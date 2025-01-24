import loader
import os
import pickle

from parser.block import Container, Element
from parser.menu_parser import parse
from renpy.ast import Label, Init, Menu

def test_parse_menu_statement():
    """
    label test:
        menu: <- this is our target block
            "Option A":
                $ a = 0
            "Option B":
                $ a = 1
    """
    expected = Container(type='menu', value='menu:', children=[Container(type='option', value='"Option A":'), Container(type='option', value='"Option B":')])

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_menu_parser.rpyc')))[1]

    assert type(decompressed[0]) == Label
    assert type(decompressed[0].block[0]) == Menu

    parsed = parse(decompressed[0].block[0])

    assert parsed.__class__ == Container
    assert expected.value == parsed.value
    assert len(expected.children) == len(parsed.children)

    for left, right in zip(expected.children, parsed.children):
        assert left.value == right.value

def test_parse_menu_statement_with_label():
    """
    menu target: <- this is our target block
        "Option A":
            $ a = 0
        "Option B":
            $ a = 1
    """
    expected = Container(type='menu', value='menu:', children=[Container(type='option', value='"Option A":'), Container(type='option', value='"Option B":')])

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_menu_parser_with_label.rpyc')))[1]

    assert type(decompressed[0]) == Label
    assert decompressed[0].name == 'target'
    assert type(decompressed[1]) == Menu

    parsed = parse(decompressed[1])

    assert parsed.__class__ == Container
    assert expected.value == parsed.value
    assert len(expected.children) == len(parsed.children)

    for left, right in zip(expected.children, parsed.children):
        assert left.value == right.value

def test_parse_menu_statement_with_menuset():
    """
    define menuset = set()

    label test:
        menu: <- this is our target block
            "Option A":
                $ a = 0
            "Option B":
                $ a = 1
    """
    expected = Container(type='menu', value='menu:', children=[Element(type='menuset', value='set menuset'), Container(type='option', value='"Option A":'), Container(type='option', value='"Option B":')])

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_menu_parser_with_menuset.rpyc')))[1]

    assert type(decompressed[0]) == Init
    assert type(decompressed[1]) == Label
    assert type(decompressed[1].block[0]) == Menu

    parsed = parse(decompressed[1].block[0])

    assert parsed.__class__ == Container
    assert expected.value == parsed.value
    assert len(expected.children) == len(parsed.children)

    for left, right in zip(expected.children, parsed.children):
        assert left.value == right.value

def test_parse_menu_statement_with_arguments():
    """
    label test:
        menu: <- this is our target block
            "Option A" if a == 1:
                $ a = 0
            "Option B":
                $ a = 1
    """
    expected = Container(type='menu', value='menu:', children=[Container(type='option', value='"Option A" if a == 1:'), Container(type='option', value='"Option B":')])

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_menu_parser_with_arguments.rpyc')))[1]

    assert type(decompressed[0]) == Label
    assert type(decompressed[0].block[0]) == Menu

    parsed = parse(decompressed[0].block[0])

    assert parsed.__class__ == Container
    assert expected.value == parsed.value
    assert len(expected.children) == len(parsed.children)

    for left, right in zip(expected.children, parsed.children):
        assert left.value == right.value
