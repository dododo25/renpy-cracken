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
