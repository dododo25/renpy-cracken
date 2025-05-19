import loader
import os
import pickle

from renpy.ast import Init, Style

def test_parse_style_statement():
    """
    style target: <- this is our target block
        xalign 0.0
    """
    expected = 'style target:'
    expected_children = ['xalign 0.0']

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_style_parser.rpyc')))[1]

    assert type(decompressed[0]) == Init
    assert type(decompressed[0].block[0]) == Style
    assert expected == str(decompressed[0].block[0])
    assert expected_children == list(map(str, decompressed[0].block[0].nchildren))

def test_parse_style_statement_with_parameters():
    """
    style target is text clear take test variant test: <- this is our target block
        xalign 0.0
    """
    expected = 'style target is text clear take test variant test:'
    expected_children = ['xalign 0.0']

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_style_parser_with_parameters.rpyc')))[1]

    assert type(decompressed[0]) == Init
    assert type(decompressed[0].block[0]) == Style
    assert expected == str(decompressed[0].block[0])
    assert expected_children == list(map(str, decompressed[0].block[0].nchildren))
