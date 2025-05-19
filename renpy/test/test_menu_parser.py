import loader
import os
import pickle

from renpy.ast import Label, Init, Menu

def test_parse_menu_statement():
    """
    label test:
        menu: <- this is our target block
            "Option A":
                $ a = 0
            "Option B":
                $ a = 1
    """
    expected = 'menu:'
    expected_children = ['"Option A":', '"Option B":']

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_menu_parser.rpyc')))[1]

    assert type(decompressed[0]) == Label
    assert type(decompressed[0].block[0]) == Menu
    assert expected == str(decompressed[0].block[0])
    assert expected_children == list(map(str, decompressed[0].block[0].nchildren))

def test_parse_menu_statement_with_label():
    """
    menu target: <- this is our target block
        "Option A":
            $ a = 0
        "Option B":
            $ a = 1
    """
    expected = 'menu:'
    expected_children = ['"Option A":', '"Option B":']

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_menu_parser_with_label.rpyc')))[1]

    assert type(decompressed[0]) == Label
    assert decompressed[0].name == 'target'
    assert type(decompressed[1]) == Menu
    assert expected == str(decompressed[1])
    assert expected_children == list(map(str, decompressed[1].nchildren))

def test_parse_menu_statement_with_menuset():
    """
    define menuset = set()

    label test:
        menu: <- this is our target block
            "Option A":
                $ a = 0
            "Option B":
                $ a = 1
    """
    expected = 'menu:'
    expected_children = ['set menuset', '"Option A":', '"Option B":']

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_menu_parser_with_menuset.rpyc')))[1]

    assert type(decompressed[1]) == Label
    assert type(decompressed[1].block[0]) == Menu
    assert expected == str(decompressed[1].block[0])
    assert expected_children == list(map(str, decompressed[1].block[0].nchildren))

def test_parse_menu_statement_with_arguments():
    """
    label test:
        menu: <- this is our target block
            "Option A" if a == 1:
                $ a = 0
            "Option B":
                $ a = 1
    """
    expected = 'menu:'
    expected_children = ['"Option A" if a == 1:', '"Option B":']

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_menu_parser_with_arguments.rpyc')))[1]

    assert type(decompressed[0]) == Label
    assert type(decompressed[0].block[0]) == Menu
    assert expected == str(decompressed[0].block[0])
    assert expected_children == list(map(str, decompressed[0].block[0].nchildren))
