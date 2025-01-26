import loader
import os
import pickle

from parser.block import Container
from parser.raw_choice_parser import parse
from renpy.ast import Label, Show
from renpy.atl import RawBlock, RawChoice

def test_parse_raw_choice_statement():
    """
    label test:
        show test:
            choice: <- this is our target block
                "target.png"
    """
    expected = Container(type='atl', value='choice:')

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_raw_choice_parser.rpyc')))[1]

    assert type(decompressed[0]) == Label
    assert type(decompressed[0].block[0]) == Show
    assert type(decompressed[0].block[0].atl) == RawBlock
    assert type(decompressed[0].block[0].atl.statements[0]) == RawChoice

    parsed = parse(decompressed[0].block[0].atl.statements[0])

    assert expected.__class__ == parsed.__class__
    assert expected.value == parsed.value
