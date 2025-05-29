import loader
import os
import pickle

from renpy.ast import TranslateBlock, Style


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
