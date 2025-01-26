import loader
import os
import pickle

from parser.block import Container
from parser.sl_if_parser import parse
from renpy.ast import Init, Screen
from renpy.sl2.slast import SLIf

def test_parse_sl_if_statement():
    """
    screen test:
        if a == 0: <- this is our target block
            add "sad.jpg"
        elif a == 1:
            add "happy.jpg"
        else:
            add "exited.jpg"
    """
    expected = Container(type='INVALID', children=[Container(type='if', value='if a == 0:'), Container(type='elif', value='elif a == 1:'), Container(type='else', value='else:')])

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_sl_if_parser.rpyc')))[1]

    assert type(decompressed[0]) == Init
    assert type(decompressed[0].block[0]) == Screen
    assert type(decompressed[0].block[0].screen.children[0]) == SLIf

    parsed = parse(decompressed[0].block[0].screen.children[0])

    assert expected.__class__ == parsed.__class__
    assert expected.value == parsed.value
    assert len(expected.children) == len(parsed.children)

    for left, right in zip(expected.children, parsed.children):
        assert left.value == right.value
