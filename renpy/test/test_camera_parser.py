import loader
import os
import pickle

from renpy.ast import Camera, Label
from renpy.atl import RawMultipurpose

def test_parse_camera_statement():
    """
    label test:
        camera target <- this is our target block
    """
    expected = 'camera target'

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_camera_parser.rpyc')))[1]

    assert type(decompressed[0]) == Label
    assert type(decompressed[0].block[0]) == Camera
    assert expected == str(decompressed[0].block[0])

def test_parse_camera_statement_with_atl():
    """
    label test:
        camera target: <- this is our target block
            align (0.0, 0.0)
    """
    expected = 'camera target:'
    expected_children = ['align (0.0, 0.0)']

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_camera_parser_with_atl.rpyc')))[1]

    assert type(decompressed[0]) == Label
    assert type(decompressed[0].block[0]) == Camera
    assert expected == str(decompressed[0].block[0])
    assert type(decompressed[0].block[0].nchildren[0]) == RawMultipurpose
    assert expected_children == list(map(str, decompressed[0].block[0].nchildren[0].nchildren))

def test_parse_camera_statement_with_at_parameter():
    """
    label test:
        camera target at master <- this is our target block
    """
    expected = 'camera target at master'

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_camera_parser_with_at_parameter.rpyc')))[1]

    assert type(decompressed[0]) == Label
    assert type(decompressed[0].block[0]) == Camera
    assert expected == str(decompressed[0].block[0])
