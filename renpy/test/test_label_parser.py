import loader
import os
import pickle

from renpy.ast import Label

def test_parse_label_statement():
    """
    label target: <- this is our target block
        pass
    """
    expected = 'label target:'

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_label_parser.rpyc')))[1]

    assert type(decompressed[0]) == Label
    assert expected == str(decompressed[0])

def test_parse_label_statement_with_parameters():
    """
    label target(a, b, c=None): <- this is our target block
        pass
    """
    expected = 'label target(a, b, c=None, *args, **kwargs):'

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_label_parser_with_parameters.rpyc')))[1]

    assert type(decompressed[0]) == Label
    assert expected == str(decompressed[0])

def test_parse_label_statement_with_hide_param():
    """
    label target hide: <- this is our target block
        pass
    """
    expected = 'label target hide:'

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_label_parser_with_hide_param.rpyc')))[1]

    assert type(decompressed[0]) == Label
    assert expected == str(decompressed[0])
