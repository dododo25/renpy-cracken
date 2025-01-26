import loader
import os
import pickle

from parser.block import Container, Element
from parser.translate_string_parser import parse
from renpy.ast import Init, TranslateString

def test_parse_translate_string_statement():
    """
    translate english strings: <- this is our target block
        old "Transalte parser test"
        new "Transalte parser test"
    """
    expected = Container(type='translate', value='translate english strings:', children=[Element(type='translation-old', value='old "Transalte parser test"'), Element(type='translation-new', value='new "Transalte parser test"')])

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_translate_string_parser.rpyc')))[1]

    assert type(decompressed[0]) == Init
    assert type(decompressed[0].block[0]) == TranslateString
    assert expected == parse(decompressed[0].block[0])
