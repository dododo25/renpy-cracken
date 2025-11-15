import loader
import os
import pickle

from renpy.ast import Label, Show
from renpy.atl import RawBlock, RawMultipurpose

def test_parse_raw_multipurpose_contains_statement():
    """
    label test:
        show test:
            "target.png" <- this is our target block
    """
    expected = 'contains:'
    expected_children = ['"target.png"']

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_raw_multipurpose_parser_as_contains_statement.rpyc')))[1]

    assert type(decompressed[0]) == Label
    assert type(decompressed[0].block[0]) == Show
    assert type(decompressed[0].block[0].atl) == RawBlock
    assert type(decompressed[0].block[0].atl.statements[0].nchildren[0]) == RawBlock
    assert type(decompressed[0].block[0].atl.statements[0].nchildren[0].statements[0]) == RawMultipurpose
    assert expected == str(decompressed[0].block[0].atl.statements[0].nchildren[0].statements[0])
    assert expected_children == list(map(str, decompressed[0].block[0].atl.statements[0]
                                         .nchildren[0].statements[0].nchildren))

def test_parse_raw_multipurpose_complex_contains_statement():
    """
    label test:
        show test:
            contains: <- this is our target block
                "target.png"
                xalign 0.0
    """
    expected1 = 'contains:'
    expected2 = 'contains:'

    expected1_children = ['"target.png"']
    expected2_children = ['xalign 0.0']

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_raw_multipurpose_parser_as_complex_contains_statement.rpyc')))[1]

    assert type(decompressed[0]) == Label
    assert type(decompressed[0].block[0]) == Show
    assert type(decompressed[0].block[0].atl) == RawBlock
    assert type(decompressed[0].block[0].atl.statements[0].nchildren[0]) == RawBlock
    assert type(decompressed[0].block[0].atl.statements[0].nchildren[0].statements[0]) == RawMultipurpose
    assert type(decompressed[0].block[0].atl.statements[0].nchildren[0].statements[1]) == RawMultipurpose
    assert expected1 == str(decompressed[0].block[0].atl.statements[0].nchildren[0].statements[0])
    assert expected2 == str(decompressed[0].block[0].atl.statements[0].nchildren[0].statements[1])
    assert expected1_children == list(map(str, decompressed[0].block[0].atl.statements[0].nchildren[0].statements[0].nchildren))
    assert expected2_children == list(map(str, decompressed[0].block[0].atl.statements[0].nchildren[0].statements[1].nchildren))

def test_parse_raw_multipurpose_block_contains_statement():
    """
    label test:
        show test:
            linear 1.0: <- this is our target block
                xalign 1.0
                yalign 1.0
    """
    expected = 'linear 1.0 xalign 1.0 yalign 1.0'

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_raw_multipurpose_parser_as_block_statement.rpyc')))[1]

    assert type(decompressed[0]) == Label
    assert type(decompressed[0].block[0]) == Show
    assert type(decompressed[0].block[0].atl) == RawBlock
    assert type(decompressed[0].block[0].atl.statements[0]) == RawMultipurpose
    assert expected == str(decompressed[0].block[0].atl.statements[0])

def test_parse_raw_multipurpose_pause_statement():
    """
    label test:
        show test:
            pause 2.0 <- this is our target block
    """
    expected = 'pause 2.0'

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_raw_multipurpose_parser_as_pause_statement.rpyc')))[1]

    assert type(decompressed[0]) == Label
    assert type(decompressed[0].block[0]) == Show
    assert type(decompressed[0].block[0].atl) == RawBlock
    assert type(decompressed[0].block[0].atl.statements[0]) == RawMultipurpose
    assert expected == str(decompressed[0].block[0].atl.statements[0])

def test_parse_raw_multipurpose_pause_statement_without_pause_keyword():
    """
    label test:
        show test:
            pause 2.0 <- this is our target block
    """
    expected = 'pause 2.0'

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_raw_multipurpose_parser_as_pause_statement_without_pause_keyword.rpyc')))[1]

    assert type(decompressed[0]) == Label
    assert type(decompressed[0].block[0]) == Show
    assert type(decompressed[0].block[0].atl) == RawBlock
    assert type(decompressed[0].block[0].atl.statements[0]) == RawMultipurpose
    assert expected == str(decompressed[0].block[0].atl.statements[0])

def test_parse_raw_multipurpose_simple_statement():
    """
    label test:
        show test:
            xalign 0.0 <- this is our target block
    """
    expected = 'contains:'
    expected_children = ['xalign 0.0']

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_raw_multipurpose_parser_as_simple_statement.rpyc')))[1]

    assert type(decompressed[0]) == Label
    assert type(decompressed[0].block[0]) == Show
    assert type(decompressed[0].block[0].atl) == RawBlock
    assert type(decompressed[0].block[0].atl.statements[0]) == RawMultipurpose
    assert expected == str(decompressed[0].block[0].atl.statements[0])
    assert expected_children == list(map(str, decompressed[0].block[0].atl.statements[0].nchildren))

def test_parse_raw_multipurpose_transition_statement():
    """
    label test:
        show test:
            xalign 0.0
            linear 1.0 xalign 1.0 <- this is our target block
    """
    expected = 'linear 1.0 xalign 1.0'

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_raw_multipurpose_parser_as_transition_statement.rpyc')))[1]

    assert type(decompressed[0]) == Label
    assert type(decompressed[0].block[0]) == Show
    assert type(decompressed[0].block[0].atl) == RawBlock
    assert type(decompressed[0].block[0].atl.statements[1]) == RawMultipurpose
    assert expected == str(decompressed[0].block[0].atl.statements[1])

def test_parse_raw_multipurpose_transition_with_warp_statement():
    """
    label test:
        show test:
            xalign 0.0
            warp xalign 0.0 1.0 <- this is our target block
    """
    expected = 'warp xalign 0.0 1.0'

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_raw_multipurpose_parser_as_transition_with_warp_statement.rpyc')))[1]

    assert type(decompressed[0]) == Label
    assert type(decompressed[0].block[0]) == Show
    assert type(decompressed[0].block[0].atl) == RawBlock
    assert type(decompressed[0].block[0].atl.statements[0]) == RawMultipurpose
    assert expected == str(decompressed[0].block[0].atl.statements[0])

def test_parse_raw_multipurpose_transition_statement_with_splines():
    """
    label test:
        show test:
            xalign 0.0
            linear 1.0 xalign 1.0 knot (0.0, .33) knot (1.0, .66) <- this is our target block
    """
    expected = 'linear 1.0 xalign 1.0 knot (0.0, .33) knot (1.0, .66)'

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_raw_multipurpose_parser_as_transition_statement_with_splines.rpyc')))[1]

    assert type(decompressed[0]) == Label
    assert type(decompressed[0].block[0]) == Show
    assert type(decompressed[0].block[0].atl) == RawBlock
    assert type(decompressed[0].block[0].atl.statements[1]) == RawMultipurpose
    assert expected == str(decompressed[0].block[0].atl.statements[1])

def test_parse_raw_multipurpose_transition_statement_with_circles():
    """
    label test:
        show test:
            xalign 0.0
            linear 1.0 xalign 1.0 circles 3 <- this is our target block
    """
    expected = 'linear 1.0 xalign 1.0 circles 3'

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_raw_multipurpose_parser_as_transition_statement_with_circles.rpyc')))[1]

    assert type(decompressed[0]) == Label
    assert type(decompressed[0].block[0]) == Show
    assert type(decompressed[0].block[0].atl) == RawBlock
    assert type(decompressed[0].block[0].atl.statements[1]) == RawMultipurpose
    assert expected == str(decompressed[0].block[0].atl.statements[1])

def test_parse_raw_multipurpose_transition_statement_with_revolution():
    """
    label test:
        show test:
            xalign 0.0
            linear 1.0 xalign 1.0 clockwise <- this is our target block
    """
    expected = 'linear 1.0 xalign 1.0 clockwise'

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_raw_multipurpose_parser_as_transition_statement_with_revolution.rpyc')))[1]

    assert type(decompressed[0]) == Label
    assert type(decompressed[0].block[0]) == Show
    assert type(decompressed[0].block[0].atl) == RawBlock
    assert type(decompressed[0].block[0].atl.statements[1]) == RawMultipurpose
    assert expected == str(decompressed[0].block[0].atl.statements[1])

def test_parse_raw_multipurpose_transition_statement_with_no_value_part():
    """
    label test:
        show test:
            xalign 0.0
            linear 1.0 truecenter <- this is our target block
    """
    expected ='linear 1.0 truecenter'

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_raw_multipurpose_parser_as_transition_statement_with_no_value_part.rpyc')))[1]

    assert type(decompressed[0]) == Label
    assert type(decompressed[0].block[0]) == Show
    assert type(decompressed[0].block[0].atl) == RawBlock
    assert type(decompressed[0].block[0].atl.statements[1]) == RawMultipurpose
    assert expected == str(decompressed[0].block[0].atl.statements[1])

def test_parse_raw_multipurpose_outlines_statement():
    """
    label test:
        show test:
            outlines [ <- this is our target block
                (absolute(1), "#000", absolute(0), absolute(0)),
                (absolute(2), "#000", absolute(1), absolute(0))
            ]
    """
    expected = '(\'outlines [\\n            (absolute(1), "#000", absolute(0), absolute(0)),\\n            (absolute(2), "#000", absolute(1), absolute(0))\\n        ]\', None)'

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_raw_multipurpose_parser_outlines_statement.rpyc')))[1]

    assert type(decompressed[0]) == Label
    assert type(decompressed[0].block[0]) == Show
    assert type(decompressed[0].block[0].atl) == RawBlock
    assert type(decompressed[0].block[0].atl.statements[0]) == RawMultipurpose
    assert expected == str(decompressed[0].block[0].atl.statements[0].expressions[0])
