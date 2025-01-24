import loader
import os
import pickle

from parser.block import Container, Element
from parser.scene_parser import parse
from renpy.ast import Label, Scene

def test_parse_scene_statement():
    """
    label test:
        scene target <- this is our target block
    """
    expected = Element(type='scene', value='scene target')

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_scene_parser.rpyc')))[1]

    assert type(decompressed[0]) == Label
    assert type(decompressed[0].block[0]) == Scene
    assert expected == parse(decompressed[0].block[0])

def test_parse_scene_statement_with_atl():
    """
    label test:
        scene target: <- this is our target block
            align (0.5, 0.5)
    """
    expected = Container(type='scene', value='scene target:')

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_scene_parser_with_atl.rpyc')))[1]

    assert type(decompressed[0]) == Label
    assert type(decompressed[0].block[0]) == Scene

    parsed = parse(decompressed[0].block[0])

    assert expected.__class__ == parsed.__class__
    assert expected.value == parsed.value

def test_parse_scene_statement_with_at_param():
    """
    label test:
        scene target at truecenter <- this is our target block
    """
    expected = Element(type='scene', value='scene target at truecenter')

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_scene_parser_with_at_param.rpyc')))[1]

    assert type(decompressed[0]) == Label
    assert type(decompressed[0].block[0]) == Scene
    assert expected == parse(decompressed[0].block[0])

def test_parse_scene_statement_with_as_param():
    """
    label test:
        scene expression Frame("test.jpg") as target <- this is our target block
    """
    expected = Element(type='scene', value='scene expression Frame("test.jpg") as target')

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_scene_parser_with_as_param.rpyc')))[1]

    assert type(decompressed[0]) == Label
    assert type(decompressed[0].block[0]) == Scene
    assert expected == parse(decompressed[0].block[0])
