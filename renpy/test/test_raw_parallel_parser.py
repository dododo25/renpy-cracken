import loader
import os
import pickle

from renpy.ast import Label, Show
from renpy.atl import RawBlock, RawParallel

def test_parse_raw_parallel_statement():
    """
    label test:
        show test:
            xalign 0.0

            parallel: <- this is our target block
                linear 1.0 xalign 1.0
                linear 1.0 xalign 0.0
    """
    expected = 'parallel:'
    expected_children = ['linear 1.0 xalign 1.0', 'linear 1.0 xalign 0.0']

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_raw_parallel_parser.rpyc')))[1]

    assert type(decompressed[0]) == Label
    assert type(decompressed[0].block[0]) == Show
    assert type(decompressed[0].block[0].atl) == RawBlock
    assert type(decompressed[0].block[0].atl.statements[1]) == RawParallel
    assert expected == str(decompressed[0].block[0].atl.statements[1])
    assert type(decompressed[0].block[0].atl.statements[1].nchildren[0]) == RawBlock
    assert expected_children == list(map(str, decompressed[0].block[0].atl.statements[1].nchildren[0].nchildren))
