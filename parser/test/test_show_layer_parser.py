import decompressor
import os

from parser.block import Container, Element
from parser.show_layer_parser import parse
from renpy.ast import Label, ShowLayer

def test_parse_show_layer_statement():
    """
    label test:
        show layer target <- this is our target block
    """
    expected = Element(type='show', value='show layer target')

    decompressed = decompressor.decompress(os.path.join(os.path.dirname(__file__), 'test_show_layer_parser.rpyc'))

    assert type(decompressed[0]) == Label
    assert type(decompressed[0].block[0]) == ShowLayer
    assert expected == parse(decompressed[0].block[0])

def test_parse_show_layer_statement_with_atl():
    """
    label test:
        show layer target: <- this is our target block
            blur 10
    """
    expected = Container(type='show', value='show layer target:')

    decompressed = decompressor.decompress(os.path.join(os.path.dirname(__file__), 'test_show_layer_parser_with_atl.rpyc'))

    assert type(decompressed[0]) == Label
    assert type(decompressed[0].block[0]) == ShowLayer

    parsed = parse(decompressed[0].block[0])

    assert parsed.__class__ == Container
    assert expected.value == parsed.value

def test_parse_show_layer_statement_with_at_parameter():
    """
    label test:
        show layer target at master <- this is our target block
    """
    expected = Element(type='show', value='show layer target at master')

    decompressed = decompressor.decompress(os.path.join(os.path.dirname(__file__), 'test_show_layer_parser_with_at_parameter.rpyc'))

    assert type(decompressed[0]) == Label
    assert type(decompressed[0].block[0]) == ShowLayer
    assert expected == parse(decompressed[0].block[0])
