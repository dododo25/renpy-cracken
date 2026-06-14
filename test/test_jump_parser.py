import loader
import os
import pickle

from renpy.ast import Label, Jump

def test_parse_jump_statement():
    """
    label test:
        jump target <- this is our target block

    label target:
        pass
    """
    expected = 'jump target'

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_jump_parser.rpyc')))[1]

    assert type(decompressed[0]) == Label
    assert type(decompressed[0].block[0]) == Jump
    assert expected == str(decompressed[0].block[0])
