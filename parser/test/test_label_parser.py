import loader
import os
import pickle

from parser.block import Container
from parser.label_parser import parse
from renpy.ast import Label

def test_parse_label_statement():
    """
    label target: <- this is our target block
        pass
    """
    expected = Container(type='label', value='label target:')

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_label_parser.rpyc')))[1]

    assert type(decompressed[0]) == Label

    parsed = parse(decompressed[0])

    assert parsed.__class__ == Container
    assert expected.value == parsed.value

def test_parse_label_statement_with_parameters():
    """
    label target(a, b, c=None): <- this is our target block
        pass
    """
    expected = Container(type='label', value='label target(a, b, c=None, *args, **kwargs):')

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_label_parser_with_parameters.rpyc')))[1]

    assert type(decompressed[0]) == Label

    parsed = parse(decompressed[0])

    assert parsed.__class__ == Container
    assert expected.value == parsed.value

def test_parse_label_statement_with_hide_param():
    """
    label target hide: <- this is our target block
        pass
    """
    expected = Container(type='label', value='label target hide:')

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_label_parser_with_hide_param.rpyc')))[1]

    assert type(decompressed[0]) == Label

    parsed = parse(decompressed[0])

    assert parsed.__class__ == Container
    assert expected.value == parsed.value
