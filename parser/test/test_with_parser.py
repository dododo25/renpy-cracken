import loader
import os
import pickle

from parser.block import Element
from parser.with_parser import parse
from renpy.ast import Label, With

def test_parse_with_statement():
    """
    label test:
        with dissolve <- this is our target block
    """
    expected = Element(type='with', value='with dissolve')

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_with_parser.rpyc')))[1]

    assert type(decompressed[0]) == Label
    assert type(decompressed[0].block[0]) == With
    assert expected == parse(decompressed[0].block[0])
