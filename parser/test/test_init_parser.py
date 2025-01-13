import decompressor
import os

from parser.block import Container
from parser.init_parser import parse
from renpy.ast import Init

def test_parse_init_statement():
    """
    init: <- this is our target block
        $ propery = 'test'
    """
    expected = Container(type='init', value='init:')

    decompressed = decompressor.decompress(os.path.join(os.path.dirname(__file__), 'test_init_parser.rpyc'))

    assert type(decompressed[0]) == Init

    parsed = parse(decompressed[0])

    assert parsed.__class__ == Container
    assert expected.value == parsed.value

def test_parse_init_statement_with_priority_value():
    """
    init 1000: <- this is our target block
        $ propery = 'test'
    """
    expected = Container(type='init', value='init 1000:')

    decompressed = decompressor.decompress(os.path.join(os.path.dirname(__file__), 'test_init_parser_with_priority.rpyc'))

    assert type(decompressed[0]) == Init

    parsed = parse(decompressed[0])

    assert parsed.__class__ == Container
    assert expected.value == parsed.value
