import loader as loader
import os
import pickle

from renpy.ast import Init, Translate, TranslateBlock, TranslateString, Style


def test_parse_translate_block_statement():
    """
    translate english style default: <- this is our target block
        xalign 0.0
        yalign 0.0
    """
    expected = 'translate english style default:'
    expected_children = ['xalign 0.0', 'yalign 0.0', '']

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_translate_block_parser.rpyc')))[1]

    assert type(decompressed[0]) == TranslateBlock
    assert expected == str(decompressed[0])
    assert type(decompressed[0].nchildren[0]) == Style
    assert expected_children == list(map(str, decompressed[0].nchildren[0].nchildren))

def test_parse_translate_with_multiline_text_statements():
    """
    translate engish test_3c219e5d: <- this is our target block
        old "Test\nline"
        new \"\"\"Test
    line\"\"\"
    """
    expected = 'translate engish test_3c219e5d:'
    expected_children = ['old "Test\nline"', 'new "Test line with " symbol"']

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_translate_with_multiline_text_statements.rpyc')))[1]

    assert type(decompressed[0]) == Translate
    assert expected == str(decompressed[0])
    assert len(decompressed[0].nchildren) == 2
    assert expected_children == list(map(str, decompressed[0].nchildren))

def test_translate_string_with_multiline_text_statements():
    """
    translate english strings: <- this is our target block
        old "Test with \n special \t characters."
        new "Test with \n special \t characters."
    """
    expected = 'translate english strings:'
    expected_children = ['old "Test with \n special \t characters."', 'new "Test with \n special \t characters."']

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_translate_string_with_multiline_text_statements.rpyc')))[1]

    assert type(decompressed[0]) == Init
    assert type(decompressed[0].nchildren[0]) == TranslateString
    assert expected == str(decompressed[0].nchildren[0])
    assert len(decompressed[0].nchildren[0].nchildren) == 2
    assert expected_children == list(map(str, decompressed[0].nchildren[0].nchildren))
