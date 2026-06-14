import loader
import os
import pickle

from renpy.ast import Label, Return

def test_parse_return_statement():
    """
    label test:
        return <- this is our target block
    """
    expected = 'return'

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_return_parser.rpyc')))[1]

    assert type(decompressed[0]) == Label
    assert type(decompressed[0].block[0]) == Return
    assert expected == str(decompressed[0].block[0])

def test_parse_return_statement_with_value():
    """
    label test:
        return 1 <- this is our target block
    """
    expected = 'return 1'

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_return_parser_with_value.rpyc')))[1]

    assert type(decompressed[0]) == Label
    assert type(decompressed[0].block[0]) == Return
    assert expected == str(decompressed[0].block[0])
