import loader
import os
import pickle

from renpy.ast import Init, TranslateString

def test_parse_translate_string_statement():
    """
    translate english strings: <- this is our target block
        old "Translate parser test"
        new "Translate parser test"
    """
    expected = 'translate english strings:'
    expected_children = ['old "Translate parser test"', 'new "Translate parser test"']

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_translate_string_parser.rpyc')))[1]

    assert type(decompressed[0]) == Init
    assert type(decompressed[0].block[0]) == TranslateString
    assert expected == str(decompressed[0].block[0])
    assert expected_children == list(map(str, decompressed[0].block[0].nchildren))

def test_translate_string_with_special_characters():
    """
    translate english strings: <- this is our target block
        old "Test with \\n special \\t characters."
        new "Test with \\n special \\t characters."
    """
    expected = 'translate english strings:'
    expected_children = ['old "Test with \\n special \\t characters."', 'new "Test with \\n special \\t characters."']

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_translate_string_praser_with_special_characters.rpyc')))[1]

    assert type(decompressed[0]) == Init
    assert type(decompressed[0].nchildren[0]) == TranslateString
    assert expected == str(decompressed[0].nchildren[0])
    assert len(decompressed[0].nchildren[0].nchildren) == 2
    assert expected_children == list(map(str, decompressed[0].nchildren[0].nchildren))
