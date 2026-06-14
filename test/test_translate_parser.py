import loader
import os
import pickle

from renpy.ast import Translate

def test_parse_translate_statement():
    """
    translate english target: <- this is our target block
        "Translate parser test"
    """
    expected = 'translate english target:'
    expected_children = ['"Translate parser test"']

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_translate_parser.rpyc')))[1]

    assert type(decompressed[0]) == Translate
    assert expected == str(decompressed[0])
    assert expected_children == list(map(str, decompressed[0].nchildren))

def test_parse_translate_with_multiline_text_statements():
    """
    translate engish test_3c219e5d: <- this is our target block
        old "Test\\nline"
        new "Test line"
    """
    expected = 'translate engish test_3c219e5d:'
    expected_children = ['old "Test\\nline"', 'new "Test line with \\" symbol"']

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_translate_parser_for_phrase.rpyc')))[1]

    assert type(decompressed[0]) == Translate
    assert expected == str(decompressed[0])
    assert len(decompressed[0].nchildren) == 2
    assert expected_children == list(map(str, decompressed[0].nchildren))
