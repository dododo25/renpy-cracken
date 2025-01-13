import decompressor
import os

from parser.block import Element
from parser.return_parser import parse
from renpy.ast import Label, Return

def test_parse_return_statement():
    """
    label test:
        return <- this is our target block
    """
    expected = Element(type='return', value='return')

    decompressed = decompressor.decompress(os.path.join(os.path.dirname(__file__), 'test_return_parser.rpyc'))

    assert type(decompressed[0]) == Label
    assert type(decompressed[0].block[0]) == Return
    assert expected == parse(decompressed[0].block[0])

def test_parse_return_statement_with_value():
    """
    label test:
        return 1 <- this is our target block
    """
    expected = Element(type='return', value='return 1')

    decompressed = decompressor.decompress(os.path.join(os.path.dirname(__file__), 'test_return_parser_with_value.rpyc'))

    assert type(decompressed[0]) == Label
    assert type(decompressed[0].block[0]) == Return
    assert expected == parse(decompressed[0].block[0])
