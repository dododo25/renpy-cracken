import loader
import os
import pickle

from parser.block import Container
from parser.transform_parser import parse
from renpy.ast import Init, Transform

def test_parse_transform_statement():
    """
    transform target: <- this is our target block
        xalign 0.0
    """
    expected = Container(type='transform', value='transform target:')

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_transform_parser.rpyc')))[1]

    assert type(decompressed[0]) == Init
    assert type(decompressed[0].block[0]) == Transform

    parsed = parse(decompressed[0].block[0])

    assert expected.__class__ == parsed.__class__
    assert expected.value == parsed.value

def test_parse_transform_statement_with_parameters():
    """
    transform target(a, b=None): <- this is our target block
        xalign 0.0
    """
    expected = Container(type='transform', value='transform target(a, b=None):')

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_transform_parser_with_parameters.rpyc')))[1]

    assert type(decompressed[0]) == Init
    assert type(decompressed[0].block[0]) == Transform

    parsed = parse(decompressed[0].block[0])

    assert expected.__class__ == parsed.__class__
    assert expected.value == parsed.value
