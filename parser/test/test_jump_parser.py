import loader
import os
import pickle

from parser.block import Element
from parser.jump_parser import parse
from renpy.ast import Label, Jump

def test_parse_jump_statement():
    """
    label test:
        jump target <- this is our target block

    label target:
        pass
    """
    expected = Element(type='jump', value='jump target')

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_jump_parser.rpyc')))[1]

    assert type(decompressed[0]) == Label
    assert type(decompressed[0].block[0]) == Jump
    assert expected == parse(decompressed[0].block[0])
