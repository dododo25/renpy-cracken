import loader
import os
import pickle

from renpy.ast import Init

def test_parse_init_statement():
    """
    init: <- this is our target block
        $ propery = 'test'
    """
    expected = 'init:'

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_init_parser.rpyc')))[1]

    assert type(decompressed[0]) == Init
    assert expected == str(decompressed[0])

def test_parse_init_statement_with_priority_value():
    """
    init 1000: <- this is our target block
        $ propery = 'test'
    """
    expected = 'init 1000:'

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_init_parser_with_priority.rpyc')))[1]

    assert type(decompressed[0]) == Init
    assert expected == str(decompressed[0])
