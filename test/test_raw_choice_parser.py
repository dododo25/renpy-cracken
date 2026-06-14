import loader
import os
import pickle

from renpy.ast import Label, Show
from renpy.atl import RawBlock, RawChoice, RawMultipurpose


def test_parse_raw_choice_statement():
    """
    label test:
        show test:
            choice: <- this is our target block
                "target.png"
    """
    expected = 'choice:'
    expected_children = ['"target.png"']

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_raw_choice_parser.rpyc')))[1]

    assert type(decompressed[0]) == Label
    assert type(decompressed[0].block[0]) == Show
    assert type(decompressed[0].block[0].atl) == RawBlock
    assert type(decompressed[0].block[0].atl.statements[0]) == RawChoice
    assert expected == str(decompressed[0].block[0].atl.statements[0])
    assert type(decompressed[0].block[0].atl.statements[0].nchildren[0]) == RawBlock
    assert type(decompressed[0].block[0].atl.statements[0].nchildren[0].nchildren[0]) == RawMultipurpose
    assert expected_children == list(map(str, decompressed[0].block[0].atl.statements[0]
                                         .nchildren[0].nchildren[0].nchildren))
