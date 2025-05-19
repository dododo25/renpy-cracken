import loader
import os
import pickle

from renpy.ast import Label, Show
from renpy.atl import RawMultipurpose


def test_parse_show_statement():
    """
    label test:
        show target <- this is our target block
    """
    expected = 'show target'

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_show_parser.rpyc')))[1]

    assert type(decompressed[0]) == Label
    assert type(decompressed[0].block[0]) == Show
    assert expected == str(decompressed[0].block[0])

def test_parse_show_statement_with_atl():
    """
    label test:
        show target: <- this is our target block
            align (0.5, 0.5)
    """
    expected = 'show target:'
    expected_children = ['align (0.5, 0.5)']

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_show_parser_with_atl.rpyc')))[1]

    assert type(decompressed[0]) == Label
    assert type(decompressed[0].block[0]) == Show
    assert expected == str(decompressed[0].block[0])
    assert type(decompressed[0].block[0].nchildren[0]) == RawMultipurpose
    assert expected_children == list(map(str, decompressed[0].block[0].nchildren[0].nchildren))

def test_parse_show_statement_with_at_param():
    """
    label test:
        show target at truecenter <- this is our target block
    """
    expected = 'show target at truecenter'

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_show_parser_with_at_param.rpyc')))[1]

    assert type(decompressed[0]) == Label
    assert type(decompressed[0].block[0]) == Show
    assert expected == str(decompressed[0].block[0])

def test_parse_show_statement_with_as_param():
    """
    label test:
        show expression Frame("test.jpg") as target <- this is our target block
    """
    expected = 'show expression Frame("test.jpg") as target'

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_show_parser_with_as_param.rpyc')))[1]

    assert type(decompressed[0]) == Label
    assert type(decompressed[0].block[0]) == Show
    assert expected == str(decompressed[0].block[0])
