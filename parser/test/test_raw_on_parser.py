import loader
import os
import pickle

from parser.block import Container
from parser.raw_on_parser import parse
from renpy.ast import Label, Show
from renpy.atl import RawBlock, RawOn

def test_parse_raw_on_statement():
    """
    label test:
        show test:
            on hover, idle: <- this is our target block
                linear 1.0 zoom 1.25
                linear 1.0 zoom 1.0
    """
    expected = Container(type='atl', value='on hover, idle:')

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_raw_on_parser.rpyc')))[1]

    assert type(decompressed[0]) == Label
    assert type(decompressed[0].block[0]) == Show
    assert type(decompressed[0].block[0].atl) == RawBlock
    assert type(decompressed[0].block[0].atl.statements[0]) == RawOn

    parsed = parse(decompressed[0].block[0].atl.statements[0])

    assert expected.__class__ == parsed.__class__
    assert expected.value == parsed.value
