import loader
import os
import pickle

from parser.block import Element
from parser.raw_repeat_parser import parse
from renpy.ast import Label, Show
from renpy.atl import RawBlock, RawRepeat

def test_parse_raw_repeat_statement():
    """
    label test:
        show test:
            xalign 0.0
            linear 1.0 xalign 1.0
            linear 1.0 xalign 0.0
            repeat <- this is our target block
    """
    expected = Element(type='atl', value='repeat')

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_raw_repeat_parser.rpyc')))[1]

    assert type(decompressed[0]) == Label
    assert type(decompressed[0].block[0]) == Show
    assert type(decompressed[0].block[0].atl) == RawBlock
    assert type(decompressed[0].block[0].atl.statements[3]) == RawRepeat
    assert expected == parse(decompressed[0].block[0].atl.statements[3])

def test_parse_raw_repeat_statement_with_value():
    """
    label test:
        show test:
            xalign 0.0
            linear 1.0 xalign 1.0
            linear 1.0 xalign 0.0
            repeat 3 <- this is our target block
    """
    expected = Element(type='atl', value='repeat 3')

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_raw_repeat_parser_with_value.rpyc')))[1]

    assert type(decompressed[0]) == Label
    assert type(decompressed[0].block[0]) == Show
    assert type(decompressed[0].block[0].atl) == RawBlock
    assert type(decompressed[0].block[0].atl.statements[3]) == RawRepeat
    assert expected == parse(decompressed[0].block[0].atl.statements[3])
