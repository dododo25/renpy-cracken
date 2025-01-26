import loader
import os
import pickle

from parser.block import Container, Element
from parser.camera_parser import parse
from renpy.ast import Camera, Label

def test_parse_camera_statement():
    """
    label test:
        camera target <- this is our target block
    """
    expected = Element(type='camera', value='camera target')

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_camera_parser.rpyc')))[1]

    assert type(decompressed[0]) == Label
    assert type(decompressed[0].block[0]) == Camera
    assert expected == parse(decompressed[0].block[0])

def test_parse_camera_statement_with_atl():
    """
    label test:
        camera target: <- this is our target block
            align (0.0, 0.0)
    """
    expected = Container(type='camera', value='camera target:')

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_camera_parser_with_atl.rpyc')))[1]

    assert type(decompressed[0]) == Label
    assert type(decompressed[0].block[0]) == Camera

    parsed = parse(decompressed[0].block[0])

    assert parsed.__class__ == Container
    assert expected.value == parsed.value

def test_parse_camera_statement_with_at_parameter():
    """
    label test:
        camera target at master <- this is our target block
    """
    expected = Element(type='camera', value='camera target at master')

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_camera_parser_with_at_parameter.rpyc')))[1]

    assert type(decompressed[0]) == Label
    assert type(decompressed[0].block[0]) == Camera
    assert expected == parse(decompressed[0].block[0])
