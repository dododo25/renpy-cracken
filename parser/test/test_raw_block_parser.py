import loader
import os
import pickle

from parser.block import Container, Element
from parser.raw_block_parser import parse
from renpy.ast import Label, Show
from renpy.atl import RawBlock

def test_parse_raw_block_statement():
    """
    label test:
        show test:
            xalign 0.0

            block: <- this is our target block
                linear 1.0 xalign 1.0
                linear 1.0 xalign 0.5
                repeat
    """
    expected = Container(type='atl', value='block:', children=[Element(type='atl', value='"target.png"')])

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_raw_block_parser.rpyc')))[1]

    assert type(decompressed[0]) == Label
    assert type(decompressed[0].block[0]) == Show
    assert type(decompressed[0].block[0].atl) == RawBlock
    assert type(decompressed[0].block[0].atl.statements[1]) == RawBlock

    parsed = parse(decompressed[0].block[0].atl.statements[1])

    assert expected.__class__ == parsed.__class__
    assert expected.value == parsed.value
