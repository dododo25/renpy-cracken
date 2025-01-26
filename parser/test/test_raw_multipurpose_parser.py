import loader
import os
import pickle

from parser.block import Container, Element
from parser.raw_multipurpose_parser import parse
from renpy.ast import Label, Show
from renpy.atl import RawBlock, RawMultipurpose

def test_parse_raw_multipurpose_contains_statement():
    """
    label test:
        show test:
            "target.png" <- this is our target block
    """
    expected = Container(type='atl', value='contains:', children=[Element(type='atl', value='"target.png"')])

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_raw_multipurpose_parser_as_contains_statement.rpyc')))[1]

    assert type(decompressed[0]) == Label
    assert type(decompressed[0].block[0]) == Show
    assert type(decompressed[0].block[0].atl) == RawBlock
    assert type(decompressed[0].block[0].atl.statements[0].children[0]) == RawBlock
    assert type(decompressed[0].block[0].atl.statements[0].children[0].statements[0]) == RawMultipurpose
    assert expected == parse(decompressed[0].block[0].atl.statements[0].children[0].statements[0])

def test_parse_raw_multipurpose_complex_contains_statement():
    """
    label test:
        show test:
            contains: <- this is our target block
                "target.png"
                xalign 0.0
    """
    expected1 = Container(type='atl', value='contains:', children=[Element(type='atl', value='"target.png"')])
    expected2 = Container(type='atl', value='contains:', children=[Element(type='atl', value='xalign 0.0')])

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_raw_multipurpose_parser_as_complex_contains_statement.rpyc')))[1]

    assert type(decompressed[0]) == Label
    assert type(decompressed[0].block[0]) == Show
    assert type(decompressed[0].block[0].atl) == RawBlock
    assert type(decompressed[0].block[0].atl.statements[0].children[0]) == RawBlock
    assert type(decompressed[0].block[0].atl.statements[0].children[0].statements[0]) == RawMultipurpose
    assert type(decompressed[0].block[0].atl.statements[0].children[0].statements[1]) == RawMultipurpose
    assert expected1 == parse(decompressed[0].block[0].atl.statements[0].children[0].statements[0])
    assert expected2 == parse(decompressed[0].block[0].atl.statements[0].children[0].statements[1])

def test_parse_raw_multipurpose_block_contains_statement():
    """
    label test:
        show test:
            linear 1.0: <- this is our target block
                xalign 1.0
                yalign 1.0
    """
    expected = Element(type='atl', value='linear 1.0 xalign 1.0 yalign 1.0')

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_raw_multipurpose_parser_as_block_statement.rpyc')))[1]

    assert type(decompressed[0]) == Label
    assert type(decompressed[0].block[0]) == Show
    assert type(decompressed[0].block[0].atl) == RawBlock
    assert type(decompressed[0].block[0].atl.statements[0]) == RawMultipurpose
    assert expected == parse(decompressed[0].block[0].atl.statements[0])

def test_parse_raw_multipurpose_pause_statement():
    """
    label test:
        show test:
            pause 2.0 <- this is our target block
    """
    expected = Element(type='atl', value='pause 2.0')

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_raw_multipurpose_parser_as_pause_statement.rpyc')))[1]

    assert type(decompressed[0]) == Label
    assert type(decompressed[0].block[0]) == Show
    assert type(decompressed[0].block[0].atl) == RawBlock
    assert type(decompressed[0].block[0].atl.statements[0]) == RawMultipurpose
    assert expected == parse(decompressed[0].block[0].atl.statements[0])

def test_parse_raw_multipurpose_pause_statement_without_pause_keyword():
    """
    label test:
        show test:
            pause 2.0 <- this is our target block
    """
    expected = Element(type='atl', value='pause 2.0')

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_raw_multipurpose_parser_as_pause_statement_without_pause_keyword.rpyc')))[1]

    assert type(decompressed[0]) == Label
    assert type(decompressed[0].block[0]) == Show
    assert type(decompressed[0].block[0].atl) == RawBlock
    assert type(decompressed[0].block[0].atl.statements[0]) == RawMultipurpose
    assert expected == parse(decompressed[0].block[0].atl.statements[0])

def test_parse_raw_multipurpose_simple_statement():
    """
    label test:
        show test:
            xalign 0.0 <- this is our target block
    """
    expected = Container(type='atl', value='contains:', children=[Element(type='atl', value='xalign 0.0')])

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_raw_multipurpose_parser_as_simple_statement.rpyc')))[1]

    assert type(decompressed[0]) == Label
    assert type(decompressed[0].block[0]) == Show
    assert type(decompressed[0].block[0].atl) == RawBlock
    assert type(decompressed[0].block[0].atl.statements[0]) == RawMultipurpose
    assert expected == parse(decompressed[0].block[0].atl.statements[0])

def test_parse_raw_multipurpose_transition_statement():
    """
    label test:
        show test:
            xalign 0.0
            linear 1.0 xalign 1.0 <- this is our target block
    """
    expected = Element(type='atl', value='linear 1.0 xalign 1.0')

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_raw_multipurpose_parser_as_transition_statement.rpyc')))[1]

    assert type(decompressed[0]) == Label
    assert type(decompressed[0].block[0]) == Show
    assert type(decompressed[0].block[0].atl) == RawBlock
    assert type(decompressed[0].block[0].atl.statements[1]) == RawMultipurpose
    assert expected == parse(decompressed[0].block[0].atl.statements[1])

def test_parse_raw_multipurpose_transition_with_warp_statement():
    """
    label test:
        show test:
            xalign 0.0
            warp xalign 0.0 1.0 <- this is our target block
    """
    expected = Element(type='atl', value='warp xalign 0.0 1.0')

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_raw_multipurpose_parser_as_transition_with_warp_statement.rpyc')))[1]

    assert type(decompressed[0]) == Label
    assert type(decompressed[0].block[0]) == Show
    assert type(decompressed[0].block[0].atl) == RawBlock
    assert type(decompressed[0].block[0].atl.statements[0]) == RawMultipurpose
    assert expected == parse(decompressed[0].block[0].atl.statements[0])

def test_parse_raw_multipurpose_transition_statement_with_splines():
    """
    label test:
        show test:
            xalign 0.0
            linear 1.0 xalign 1.0 knot (0.0, .33) knot (1.0, .66) <- this is our target block
    """
    expected = Element(type='atl', value='linear 1.0 xalign 1.0 knot (0.0, .33) knot (1.0, .66)')

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_raw_multipurpose_parser_as_transition_statement_with_splines.rpyc')))[1]

    assert type(decompressed[0]) == Label
    assert type(decompressed[0].block[0]) == Show
    assert type(decompressed[0].block[0].atl) == RawBlock
    assert type(decompressed[0].block[0].atl.statements[1]) == RawMultipurpose
    assert expected == parse(decompressed[0].block[0].atl.statements[1])

def test_parse_raw_multipurpose_transition_statement_with_circles():
    """
    label test:
        show test:
            xalign 0.0
            linear 1.0 xalign 1.0 circles 3 <- this is our target block
    """
    expected = Element(type='atl', value='linear 1.0 xalign 1.0 circles 3')

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_raw_multipurpose_parser_as_transition_statement_with_circles.rpyc')))[1]

    assert type(decompressed[0]) == Label
    assert type(decompressed[0].block[0]) == Show
    assert type(decompressed[0].block[0].atl) == RawBlock
    assert type(decompressed[0].block[0].atl.statements[1]) == RawMultipurpose
    assert expected == parse(decompressed[0].block[0].atl.statements[1])

def test_parse_raw_multipurpose_transition_statement_with_revolution():
    """
    label test:
        show test:
            xalign 0.0
            linear 1.0 xalign 1.0 clockwise <- this is our target block
    """
    expected = Element(type='atl', value='linear 1.0 xalign 1.0 clockwise')

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_raw_multipurpose_parser_as_transition_statement_with_revolution.rpyc')))[1]

    assert type(decompressed[0]) == Label
    assert type(decompressed[0].block[0]) == Show
    assert type(decompressed[0].block[0].atl) == RawBlock
    assert type(decompressed[0].block[0].atl.statements[1]) == RawMultipurpose
    assert expected == parse(decompressed[0].block[0].atl.statements[1])

def test_parse_raw_multipurpose_transition_statement_with_no_value_part():
    """
    label test:
        show test:
            xalign 0.0
            linear 1.0 truecenter <- this is our target block
    """
    expected = Element(type='atl', value='linear 1.0 truecenter')

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_raw_multipurpose_parser_as_transition_statement_with_no_value_part.rpyc')))[1]

    assert type(decompressed[0]) == Label
    assert type(decompressed[0].block[0]) == Show
    assert type(decompressed[0].block[0].atl) == RawBlock
    assert type(decompressed[0].block[0].atl.statements[1]) == RawMultipurpose
    assert expected == parse(decompressed[0].block[0].atl.statements[1])
