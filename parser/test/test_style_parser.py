import loader
import os
import pickle

from parser.block import Container, Element
from parser.style_parser import parse
from renpy.ast import Init, Style

def test_parse_style_statement():
    """
    style target: <- this is our target block
        xalign 0.0
    """
    expected = Container(type='style', value='style target:', children=[Element(type='property', value='xalign 0.0')])

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_style_parser.rpyc')))[1]

    assert type(decompressed[0]) == Init
    assert type(decompressed[0].block[0]) == Style
    assert expected == parse(decompressed[0].block[0])

def test_parse_style_statement_with_parameters():
    """
    style target is text clear take test variant test: <- this is our target block
        xalign 0.0
    """
    expected = Container(type='style', value='style target is text clear take test variant test:', children=[Element(type='property', value='xalign 0.0')])

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_style_parser_with_parameters.rpyc')))[1]

    assert type(decompressed[0]) == Init
    assert type(decompressed[0].block[0]) == Style
    assert expected == parse(decompressed[0].block[0])
