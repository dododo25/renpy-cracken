import loader
import os
import pickle

from parser.block import Container, Element
from parser.translate_block_parser import parse
from renpy.ast import TranslateBlock

def test_parse_translate_block_statement():
    """
    translate english style default: <- this is our target block
        xalign 0.0
        yalign 0.0
    """
    expected = Container(type='translate', value='translate english style default:', children=[Element(type='property', value='xalign 0.0'), Element(type='property', value='yalign 0.0')])

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_translate_block_parser.rpyc')))[1]

    assert type(decompressed[0]) == TranslateBlock
    assert expected == parse(decompressed[0])
