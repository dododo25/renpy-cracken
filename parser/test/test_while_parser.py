import decompressor
import os

from parser.block import Container
from parser.while_parser import parse
from renpy.ast import Label, While

def test_parse_if_statement():
    """
    label test:
        i = 0

        while i < 5: <- this is our target block
            i += 1
    """
    expected = Container(type='while', value='while i < 5:')

    decompressed = decompressor.decompress(os.path.join(os.path.dirname(__file__), 'test_while_parser.rpyc'))

    assert type(decompressed[0]) == Label
    assert type(decompressed[0].block[1]) == While

    parsed = parse(decompressed[0].block[1])

    assert parsed.__class__ == Container
    assert expected.value == parsed.value
