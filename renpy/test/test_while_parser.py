import loader
import os
import pickle

from renpy.ast import Label, Python, While

def test_parse_while_statement():
    """
    label test:
        i = 0

        while i < 5: <- this is our target block
            $ i += 1
    """
    expected = 'while i < 5:'
    expected_children = ['i += 1']

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_while_parser.rpyc')))[1]

    assert type(decompressed[0]) == Label
    assert type(decompressed[0].block[1]) == While
    assert expected == str(decompressed[0].block[1])
    assert type(decompressed[0].block[1].nchildren[0]) == Python
    assert expected_children == list(map(str, decompressed[0].block[1].nchildren[0].nchildren))
