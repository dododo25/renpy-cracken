import loader
import os
import pickle

from parser.block import Container
from parser.while_parser import parse
from renpy.ast import Label, While

def test_parse_while_statement():
    """
    label test:
        i = 0

        while i < 5: <- this is our target block
            i += 1
    """
    expected = Container(type='while', value='while i < 5:')

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_while_parser.rpyc')))[1]

    assert type(decompressed[0]) == Label
    assert type(decompressed[0].block[1]) == While

    parsed = parse(decompressed[0].block[1])

    assert expected.__class__ == parsed.__class__
    assert expected.value == parsed.value
