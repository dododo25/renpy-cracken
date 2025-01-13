import decompressor
import os

from parser.block import Element
from parser.default_parser import parse
from renpy.ast import Init, Default

def test_parse_default_statement():
    """
    default value = 1 <- this is our target block
    """
    expected = Element(type='default', value='default value = 1')

    decompressed = decompressor.decompress(os.path.join(os.path.dirname(__file__), 'test_default_parser.rpyc'))

    assert type(decompressed[0]) == Init
    assert type(decompressed[0].block[0]) == Default
    assert expected == parse(decompressed[0].block[0])
