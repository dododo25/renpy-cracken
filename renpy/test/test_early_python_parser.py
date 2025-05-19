import loader
import os
import pickle

from renpy.ast import Init, EarlyPython

def test_parse_early_python_statement():
    """
    init:
        python early: <- this is our target block
            value = 1
    """
    expected = 'python early:'
    expected_children = ['\nvalue = 1\n']

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_early_python_parser_inside_init_block.rpyc')))[1]

    assert type(decompressed[0]) == Init
    assert type(decompressed[0].block[0]) == EarlyPython
    assert expected == str(decompressed[0].block[0])
    assert expected_children == list(map(str, decompressed[0].block[0].nchildren))

def test_parse_init_early_python_statement():
    """
    init python early: <- this is our target block
        value = 1
    """
    expected = 'python early:'
    expected_children = ['\nvalue = 1\n']

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_early_python_parser_from_init_block.rpyc')))[1]

    assert type(decompressed[0]) == Init
    assert type(decompressed[0].block[0]) == EarlyPython
    assert expected == str(decompressed[0].block[0])
    assert expected_children == list(map(str, decompressed[0].block[0].nchildren))

def test_parse_init_early_python_statement_with_hide_and_in_params():
    """
    init:
        python early hide in another_store: <- this is our target block
            value = 1
    """
    expected = 'python early hide in another_store:'
    expected_children = ['\nvalue = 1\n']

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_early_python_parser_with_hide_and_in_params.rpyc')))[1]

    assert type(decompressed[0]) == Init
    assert type(decompressed[0].block[0]) == EarlyPython
    assert expected == str(decompressed[0].block[0])
    assert expected_children == list(map(str, decompressed[0].block[0].nchildren))
