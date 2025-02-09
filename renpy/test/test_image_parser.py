import loader
import os
import pickle

from renpy.ast import Init, Image
from renpy.atl import RawMultipurpose


def test_parse_single_line_image_statement():
    """
    init:
        image target = 'target.png' <- this is our target block
    """
    expected = 'image target = \'target.png\''

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_image_parser_from_single_statement.rpyc')))[1]

    assert type(decompressed[0]) == Init
    assert type(decompressed[0].block[0]) == Image
    assert expected == str(decompressed[0].block[0])

def test_parse_complex_image_statement():
    """
    init:
        image target: <- this is our target block
            'target.png'
    """
    expected = 'image target:'
    expected_children = ['\'target.png\'']

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_image_parser_from_complex_statement.rpyc')))[1]

    assert type(decompressed[0]) == Init
    assert type(decompressed[0].block[0]) == Image
    assert expected == str(decompressed[0].block[0])
    assert type(decompressed[0].block[0].nchildren[0]) == RawMultipurpose
    assert expected_children == list(map(str, decompressed[0].block[0].nchildren[0].nchildren))
