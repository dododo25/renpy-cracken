import decompressor
import os

from parser.block import Element
from parser.define_parser import parse
from renpy.ast import Init, Define

def test_parse_define_statement():
    """
    define value = 1 <- this is our target block
    """
    expected = Element(type='define', value='define value = 1')

    decompressed = decompressor.decompress(os.path.join(os.path.dirname(__file__), 'test_define_parser.rpyc'))

    assert type(decompressed[0]) == Init
    assert type(decompressed[0].block[0]) == Define
    assert expected == parse(decompressed[0].block[0])
