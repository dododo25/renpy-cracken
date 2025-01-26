import loader
import os
import pickle

from parser.block import Element
from parser.raw_function_parser import parse
from renpy.ast import Label, Show
from renpy.atl import RawBlock, RawFunction

def test_parse_raw_function_statement():
    """
    label test:
        show test:
            function target <- this is our target block
    """
    expected = Element(type='atl', value='function target')

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_raw_function_parser.rpyc')))[1]

    assert type(decompressed[0]) == Label
    assert type(decompressed[0].block[0]) == Show
    assert type(decompressed[0].block[0].atl) == RawBlock
    assert type(decompressed[0].block[0].atl.statements[0]) == RawFunction
    assert expected == parse(decompressed[0].block[0].atl.statements[0])
