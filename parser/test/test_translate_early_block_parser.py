import loader
import os
import pickle

from parser.block import Container
from parser.translate_early_block_parser import parse
from renpy.ast import TranslateEarlyBlock

def test_parse_translate_early_block_statement():
    """
    translate english python: <- this is our target block
        "Transalte parser test"
    """
    expected = Container(type='translate', value='translate english python:')

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_translate_early_block_parser.rpyc')))[1]

    assert type(decompressed[0]) == TranslateEarlyBlock

    parsed = parse(decompressed[0])

    assert expected.__class__ == parsed.__class__
    assert expected.value == parsed.value
