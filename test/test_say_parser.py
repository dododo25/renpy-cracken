import loader
import os
import pickle

from renpy.ast import Label, Say

def test_parse_say_statement_without_character():
    """
    label test:
        "A line of dialoge without character" <- this is our target block
    """
    expected = '"A line of dialoge without character"'

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_say_parser_without_character.rpyc')))[1]

    assert type(decompressed[0]) == Label
    assert type(decompressed[0].block[0]) == Say
    assert expected == str(decompressed[0].block[0])

def test_parse_say_statement_with_style_params():
    """
    label test:
        "A line of dialoge without character" with vpunch <- this is our target block
    """
    expected = '"A line of dialoge without character" with vpunch'

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_say_parser_with_style_params.rpyc')))[1]

    assert type(decompressed[0]) == Label
    assert type(decompressed[0].block[0]) == Say
    assert expected == str(decompressed[0].block[0])

def test_parse_say_statement_with_arguments():
    """
    label test:
        "A line of dialoge without character" (what_color="#8c8") <- this is our target block
    """
    expected = '"A line of dialoge without character" (what_color="#8c8")'

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_say_parser_with_arguments.rpyc')))[1]

    assert type(decompressed[0]) == Label
    assert type(decompressed[0].block[0]) == Say
    assert expected == str(decompressed[0].block[0])

def test_parse_say_statement_with_character():
    """
    label test:
        e "A line of dialoge with character" <- this is our target block
    """
    expected = 'e "A line of dialoge with character"'

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_say_parser_with_character.rpyc')))[1]

    assert type(decompressed[0]) == Label
    assert type(decompressed[0].block[0]) == Say
    assert expected == str(decompressed[0].block[0])

def test_parse_say_statement_with_character_and_params():
    """
    label test:
        e happy "A line of dialoge with character" <- this is our target block
    """
    expected = 'e happy "A line of dialoge with character"'

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_say_parser_with_character_and_params.rpyc')))[1]

    assert type(decompressed[0]) == Label
    assert type(decompressed[0].block[0]) == Say
    assert expected == str(decompressed[0].block[0])
