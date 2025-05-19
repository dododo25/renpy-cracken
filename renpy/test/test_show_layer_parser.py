import loader
import os
import pickle

from renpy.ast import Label, ShowLayer
from renpy.atl import RawMultipurpose


def test_parse_show_layer_statement():
    """
    label test:
        show layer target <- this is our target block
    """
    expected = 'show layer target'

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_show_layer_parser.rpyc')))[1]

    assert type(decompressed[0]) == Label
    assert type(decompressed[0].block[0]) == ShowLayer
    assert expected == str(decompressed[0].block[0])

def test_parse_show_layer_statement_with_atl():
    """
    label test:
        show layer target: <- this is our target block
            blur 10
    """
    expected = 'show layer target:'
    expected_children = ['blur 10']

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_show_layer_parser_with_atl.rpyc')))[1]

    assert type(decompressed[0]) == Label
    assert type(decompressed[0].block[0]) == ShowLayer
    assert expected == str(decompressed[0].block[0])
    assert type(decompressed[0].block[0].nchildren[0]) == RawMultipurpose
    assert expected_children == list(map(str, decompressed[0].block[0].nchildren[0].nchildren))

def test_parse_show_layer_statement_with_at_parameter():
    """
    label test:
        show layer target at master <- this is our target block
    """
    expected = 'show layer target at master'

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_show_layer_parser_with_at_parameter.rpyc')))[1]

    assert type(decompressed[0]) == Label
    assert type(decompressed[0].block[0]) == ShowLayer
    assert expected == str(decompressed[0].block[0])
