import loader
import os
import pickle

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
    expected = 'on hover, idle:'
    expected_children = ['linear 1.0 zoom 1.25', 'linear 1.0 zoom 1.0']

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_raw_on_parser.rpyc')))[1]

    assert type(decompressed[0]) == Label
    assert type(decompressed[0].block[0]) == Show
    assert type(decompressed[0].block[0].atl) == RawBlock
    assert type(decompressed[0].block[0].atl.statements[0]) == RawOn
    assert expected == str(decompressed[0].block[0].atl.statements[0])
    assert expected_children == list(map(str, decompressed[0].block[0].atl.statements[0].nchildren))
