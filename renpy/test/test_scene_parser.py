import loader
import os
import pickle

from renpy.ast import Label, Scene
from renpy.atl import RawMultipurpose


def test_parse_scene_statement():
    """
    label test:
        scene target <- this is our target block
    """
    expected = 'scene target'

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_scene_parser.rpyc')))[1]

    assert type(decompressed[0]) == Label
    assert type(decompressed[0].block[0]) == Scene
    assert expected == str(decompressed[0].block[0])

def test_parse_scene_statement_with_atl():
    """
    label test:
        scene target: <- this is our target block
            align (0.5, 0.5)
    """
    expected = 'scene target:'
    expected_children = ['align (0.5, 0.5)']

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_scene_parser_with_atl.rpyc')))[1]

    assert type(decompressed[0]) == Label
    assert type(decompressed[0].block[0]) == Scene
    assert expected == str(decompressed[0].block[0])
    assert type(decompressed[0].block[0].nchildren[0]) == RawMultipurpose
    assert expected_children == list(map(str, decompressed[0].block[0].nchildren[0].nchildren))

def test_parse_scene_statement_with_at_param():
    """
    label test:
        scene target at truecenter <- this is our target block
    """
    expected = 'scene target at truecenter'

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_scene_parser_with_at_param.rpyc')))[1]

    assert type(decompressed[0]) == Label
    assert type(decompressed[0].block[0]) == Scene
    assert expected == str(decompressed[0].block[0])

def test_parse_scene_statement_with_as_param():
    """
    label test:
        scene expression Frame("test.jpg") as target <- this is our target block
    """
    expected = 'scene expression Frame("test.jpg") as target'

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_scene_parser_with_as_param.rpyc')))[1]

    assert type(decompressed[0]) == Label
    assert type(decompressed[0].block[0]) == Scene
    assert expected == str(decompressed[0].block[0])
