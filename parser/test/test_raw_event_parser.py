import loader
import os
import pickle

from parser.block import Element
from parser.raw_event_parser import parse
from renpy.ast import Label, Show
from renpy.atl import RawBlock, RawEvent

def test_parse_raw_event_statement():
    """
    label test:
        show test:
            event hide <- this is our target block
    """
    expected = Element(type='atl', value='event hide')

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_raw_event_parser.rpyc')))[1]

    assert type(decompressed[0]) == Label
    assert type(decompressed[0].block[0]) == Show
    assert type(decompressed[0].block[0].atl) == RawBlock
    assert type(decompressed[0].block[0].atl.statements[0]) == RawEvent
    assert expected == parse(decompressed[0].block[0].atl.statements[0])
