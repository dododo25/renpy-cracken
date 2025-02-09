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
