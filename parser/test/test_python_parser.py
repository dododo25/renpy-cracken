import decompressor
import os

from parser.block import Container, Element
from parser.python_parser import parse
from renpy.ast import Init, Python

def test_parse_python_statement():
    """
    init:
        python: <- this is our target block
            value = 1
    """
    expected = Container(type='python', value='python:', children=[Element(type='code', value='value = 1')])

    decompressed = decompressor.decompress(os.path.join(os.path.dirname(__file__), 'test_python_parser_inside_init_block.rpyc'))

    assert type(decompressed[0]) == Init
    assert type(decompressed[0].block[0]) == Python
    assert expected == parse(decompressed[0].block[0])

def test_parse_init_python_statement():
    """
    init python: <- this is our target block
        value = 1
    """
    expected = Container(type='python', value='python:', children=[Element(type='code', value='value = 1')])

    decompressed = decompressor.decompress(os.path.join(os.path.dirname(__file__), 'test_python_parser_from_init_block.rpyc'))

    assert type(decompressed[0]) == Init
    assert type(decompressed[0].block[0]) == Python
    assert expected == parse(decompressed[0].block[0])

def test_parse_init_python_statement_with_hide_and_in_params():
    """
    init:
        python hide in another_store: <- this is our target block
            value = 1
    """
    expected = Container(type='python', value='python hide in another_store:', children=[Element(type='code', value='value = 1')])

    decompressed = decompressor.decompress(os.path.join(os.path.dirname(__file__), 'test_python_parser_with_hide_and_in_params.rpyc'))

    assert type(decompressed[0]) == Init
    assert type(decompressed[0].block[0]) == Python
    assert expected == parse(decompressed[0].block[0])
