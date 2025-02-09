import loader
import os
import pickle

from renpy.ast import Label, If

def test_parse_if_statement():
    """
    label test:
        if a == 0: <- this is our target block
            show sad
        elif a == 1:
            show happy
        else:
            show exited
    """

    expected_children = ['if a == 0:', 'elif a == 1:', 'else:']

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_if_parser.rpyc')))[1]

    assert type(decompressed[0]) == Label
    assert type(decompressed[0].block[0]) == If
    assert decompressed[0].block[0].nexclude
    assert expected_children == list(map(str, decompressed[0].block[0].nchildren))
