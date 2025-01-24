import loader
import os
import pickle

from parser.block import Element
from parser.hide_parser import parse
from renpy.ast import Label, Hide

def test_parse_hide_statement():
    """
    init:
        image a = "test.png"

    label test:
        hide a <- this is our target block
    """
    expected = Element(type='hide', value='hide a')

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_hide_parser.rpyc')))[1]

    assert type(decompressed[1]) == Label
    assert type(decompressed[1].block[0]) == Hide
    assert expected == parse(decompressed[1].block[0])
