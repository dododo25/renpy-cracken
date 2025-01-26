import loader
import os
import pickle

from parser.block import Container
from parser.translate_parser import parse
from renpy.ast import Translate

def test_parse_translate_statement():
    """
    translate english target: <- this is our target block
        "Transalte parser test"
    """
    expected = Container(type='translate', value='translate english target:')

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_translate_parser.rpyc')))[1]

    assert type(decompressed[0]) == Translate

    parsed = parse(decompressed[0])

    assert expected.__class__ == parsed.__class__
    assert expected.value == parsed.value
