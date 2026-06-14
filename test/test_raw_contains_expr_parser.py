import loader
import os
import pickle

from renpy.ast import Label, Show
from renpy.atl import RawBlock, RawContainsExpr

def test_parse_raw_contains_expr_statement():
    """
    label test:
        show test:
            contains target <- this is our target block
    """
    expected = 'contains target'

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_raw_contains_expr_parser.rpyc')))[1]

    assert type(decompressed[0]) == Label
    assert type(decompressed[0].block[0]) == Show
    assert type(decompressed[0].block[0].atl) == RawBlock
    assert type(decompressed[0].block[0].atl.statements[0]) == RawContainsExpr
    assert expected == str(decompressed[0].block[0].atl.statements[0])
