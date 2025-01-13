import decompressor
import os

from parser.block import Container
from parser.if_parser import parse
from renpy.ast import Label, If

def test_parse_if_statement():
    """
    label test:
        if a == 0: <- this is our target block
            show sad
        elif a == 1:
            show happy
        else:
            show exited
    """
    expected = Container(type='INVALID', children=[Container(type='if', value='if a == 0:'), Container(type='elif', value='elif a == 1:'), Container(type='else', value='else:')])

    decompressed = decompressor.decompress(os.path.join(os.path.dirname(__file__), 'test_if_parser.rpyc'))

    assert type(decompressed[0]) == Label
    assert type(decompressed[0].block[0]) == If

    parsed = parse(decompressed[0].block[0])

    assert parsed.__class__ == Container
    assert expected.value == parsed.value
    assert len(expected.children) == len(parsed.children)

    for left, right in zip(expected.children, parsed.children):
        assert left.value == right.value
