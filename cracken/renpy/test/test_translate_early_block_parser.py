import loader
import os
import pickle

from renpy.ast import TranslateEarlyBlock, Python

def test_parse_translate_early_block_statement():
    """
    translate english python: <- this is our target block
        "Translate parser test"
    """
    expected ='translate english python:'
    expected_children = ['\n"Translate parser test"\n']

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_translate_early_block_parser.rpyc')))[1]

    assert type(decompressed[0]) == TranslateEarlyBlock
    assert expected == str(decompressed[0])
    assert type(decompressed[0].nchildren[0]) == Python
    assert expected_children == list(map(str, decompressed[0].nchildren[0].nchildren))
