import loader
import os
import pickle

from parser.block import Container, Element
from parser.image_parser import parse
from renpy.ast import Init, Image

def test_parse_single_line_image_statement():
    """
    init:
        image target = 'target.png' <- this is our target block
    """
    expected = Element(type='image', value='image target = \'target.png\'')

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_image_parser_from_single_statement.rpyc')))[1]

    assert type(decompressed[0]) == Init
    assert type(decompressed[0].block[0]) == Image
    assert expected == parse(decompressed[0].block[0])

def test_parse_complex_image_statement():
    """
    init:
        image target: <- this is our target block
            'target.png'
    """
    expected = Container(type='image', value='image target:')

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_image_parser_from_complex_statement.rpyc')))[1]

    assert type(decompressed[0]) == Init
    assert type(decompressed[0].block[0]) == Image

    parsed = parse(decompressed[0].block[0])

    assert parsed.__class__ == Container
    assert expected.value == parsed.value
