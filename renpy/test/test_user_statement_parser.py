import loader
import os
import pickle

from renpy.ast import Label, UserStatement

def test_parse_user_statement_window_show():
    """
    label test:
        window show <- this is our target block
    """
    expected = 'window show'

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_user_statement_parser_window_show.rpyc')))[1]

    assert type(decompressed[0]) == Label
    assert type(decompressed[0].block[0]) == UserStatement
    assert expected == str(decompressed[0].block[0])

def test_parse_user_statement_window_hide():
    """
    label test:
        window show <- this is our target block
    """
    expected = 'window hide'

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_user_statement_parser_window_hide.rpyc')))[1]

    assert type(decompressed[0]) == Label
    assert type(decompressed[0].block[0]) == UserStatement
    assert expected == str(decompressed[0].block[0])

def test_parse_user_statement_window_auto():
    """
    label test:
        window auto <- this is our target block
    """
    expected = 'window auto'

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_user_statement_parser_window_auto.rpyc')))[1]

    assert type(decompressed[0]) == Label
    assert type(decompressed[0].block[0]) == UserStatement
    assert expected == str(decompressed[0].block[0])

def test_parse_user_statement_pause():
    """
    label test:
        pause 1.0 <- this is our target block
    """
    expected = 'pause 1.0'

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_user_statement_parser_pause.rpyc')))[1]

    assert type(decompressed[0]) == Label
    assert type(decompressed[0].block[0]) == UserStatement
    assert expected == str(decompressed[0].block[0])
