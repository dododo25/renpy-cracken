import loader
import os
import pickle

from renpy.ast import Init, Transform
from renpy.atl import RawMultipurpose


def test_parse_transform_statement():
    """
    transform target: <- this is our target block
        xalign 0.0
    """
    expected = 'transform target:'
    expected_children = ['xalign 0.0']

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_transform_parser.rpyc')))[1]

    assert type(decompressed[0]) == Init
    assert type(decompressed[0].block[0]) == Transform
    assert expected == str(decompressed[0].block[0])
    assert type(decompressed[0].block[0].nchildren[0]) == RawMultipurpose
    assert expected_children == list(map(str, decompressed[0].block[0].nchildren[0].nchildren))

def test_parse_transform_statement_with_parameters():
    """
    transform target(a, b=None): <- this is our target block
        xalign 0.0
    """
    expected = 'transform target(a, b=None):'
    expected_children = ['xalign 0.0']

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_transform_parser_with_parameters.rpyc')))[1]

    assert type(decompressed[0]) == Init
    assert type(decompressed[0].block[0]) == Transform
    assert expected == str(decompressed[0].block[0])
    assert type(decompressed[0].block[0].nchildren[0]) == RawMultipurpose
    assert expected_children == list(map(str, decompressed[0].block[0].nchildren[0].nchildren))
