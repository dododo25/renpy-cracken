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

    expected_children = ['if a == 0:', 'elif a == 1:', 'else:', '']
    expected_children_children = [['show sad'], ['show happy'], ['show exited'], None]

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_if_parser.rpyc')))[1]

    assert type(decompressed[0]) == Label
    assert type(decompressed[0].block[0]) == If
    assert decompressed[0].block[0].nexclude
    assert expected_children == list(map(str, decompressed[0].block[0].nchildren))
    assert expected_children_children == list(map(lambda part: list(map(str, part.nchildren)) if part.nchildren else None, \
                                                  decompressed[0].block[0].nchildren))
