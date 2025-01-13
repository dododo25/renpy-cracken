import decompressor
import os

from parser.block import Element
from parser.say_parser import parse
from renpy.ast import Label, Say

def test_parse_say_statement_without_character():
    """
    label test:
        "A line of dialoge without character" <- this is our target block
    """
    expected = Element(type='say', value='"A line of dialoge without character"')

    decompressed = decompressor.decompress(os.path.join(os.path.dirname(__file__), 'test_say_parser_without_character.rpyc'))

    assert type(decompressed[0]) == Label
    assert type(decompressed[0].block[0]) == Say
    assert expected == parse(decompressed[0].block[0])

def test_parse_say_statement_with_style_params():
    """
    label test:
        "A line of dialoge without character" with vpunch <- this is our target block
    """
    expected = Element(type='say', value='"A line of dialoge without character" with vpunch')

    decompressed = decompressor.decompress(os.path.join(os.path.dirname(__file__), 'test_say_parser_with_style_params.rpyc'))

    assert type(decompressed[0]) == Label
    assert type(decompressed[0].block[0]) == Say
    assert expected == parse(decompressed[0].block[0])

def test_parse_say_statement_with_arguments():
    """
    label test:
        "A line of dialoge without character" (what_color="#8c8") <- this is our target block
    """
    expected = Element(type='say', value='"A line of dialoge without character" (what_color="#8c8")')

    decompressed = decompressor.decompress(os.path.join(os.path.dirname(__file__), 'test_say_parser_with_arguments.rpyc'))

    assert type(decompressed[0]) == Label
    assert type(decompressed[0].block[0]) == Say
    assert expected == parse(decompressed[0].block[0])

def test_parse_say_statement_with_character():
    """
    label test:
        e "A line of dialoge with character" <- this is our target block
    """
    expected = Element(type='say', value='e "A line of dialoge with character"')

    decompressed = decompressor.decompress(os.path.join(os.path.dirname(__file__), 'test_say_parser_with_character.rpyc'))

    assert type(decompressed[0]) == Label
    assert type(decompressed[0].block[0]) == Say
    assert expected == parse(decompressed[0].block[0])

def test_parse_say_statement_with_character_and_params():
    """
    label test:
        e happy "A line of dialoge with character" <- this is our target block
    """
    expected = Element(type='say', value='e happy "A line of dialoge with character"')

    decompressed = decompressor.decompress(os.path.join(os.path.dirname(__file__), 'test_say_parser_with_character_and_params.rpyc'))

    assert type(decompressed[0]) == Label
    assert type(decompressed[0].block[0]) == Say
    assert expected == parse(decompressed[0].block[0])
