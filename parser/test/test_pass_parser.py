import decompressor
import os

from parser.block import Element
from parser.pass_parser import parse
from renpy.ast import Label, Pass

def test_parse_pass_statement():
    """
    label test:
        pass <- this is our target block
    """
    expected = Element(type='pass', value='pass')

    decompressed = decompressor.decompress(os.path.join(os.path.dirname(__file__), 'test_pass_parser.rpyc'))

    assert type(decompressed[0]) == Label
    assert type(decompressed[0].block[0]) == Pass
    assert expected == parse(decompressed[0].block[0])
