import decompressor
import os

from parser.block import Container, Element
from parser.show_parser import parse
from renpy.ast import Label, Show

def test_parse_show_statement():
    """
    label test:
        show target <- this is our target block
    """
    expected = Element(type='show', value='show target')

    decompressed = decompressor.decompress(os.path.join(os.path.dirname(__file__), 'test_show_parser.rpyc'))

    assert type(decompressed[0]) == Label
    assert type(decompressed[0].block[0]) == Show
    assert expected == parse(decompressed[0].block[0])

def test_parse_show_statement_with_atl():
    """
    label test:
        show target: <- this is our target block
            align (0.5, 0.5)
    """
    expected = Container(type='show', value='show target:')

    decompressed = decompressor.decompress(os.path.join(os.path.dirname(__file__), 'test_show_parser_with_atl.rpyc'))

    assert type(decompressed[0]) == Label
    assert type(decompressed[0].block[0]) == Show

    parsed = parse(decompressed[0].block[0])

    assert parsed.__class__ == Container
    assert expected.value == parsed.value

def test_parse_show_statement_with_at_param():
    """
    label test:
        show target at truecenter <- this is our target block
    """
    expected = Element(type='show', value='show target at truecenter')

    decompressed = decompressor.decompress(os.path.join(os.path.dirname(__file__), 'test_show_parser_with_at_param.rpyc'))

    assert type(decompressed[0]) == Label
    assert type(decompressed[0].block[0]) == Show
    assert expected == parse(decompressed[0].block[0])

def test_parse_show_statement_with_as_param():
    """
    label test:
        show expression Frame("test.jpg") as target <- this is our target block
    """
    expected = Element(type='show', value='show expression Frame("test.jpg") as target')

    decompressed = decompressor.decompress(os.path.join(os.path.dirname(__file__), 'test_show_parser_with_as_param.rpyc'))

    assert type(decompressed[0]) == Label
    assert type(decompressed[0].block[0]) == Show
    assert expected == parse(decompressed[0].block[0])
