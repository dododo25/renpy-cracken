import loader
import os
import pickle

from renpy.ast import Label, Call

def test_parse_call_statement_no_arguments():
    """
    label test:
        call target <- this is our target block

    label target:
        pass
    """
    expected = 'call target'

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_call_parser_no_arguments.rpyc')))[1]

    assert type(decompressed[0]) == Label
    assert type(decompressed[0].block[0]) == Call
    assert expected == str(decompressed[0].block[0])

def test_parse_call_statement_with_arguments():
    """
    label test:
        call target(True, *[True, False], **{\'value\': True}) <- this is our target block

    label target(value):
        pass
    """
    expected = 'call target(True, *[True, False], **{\'value\': True})'

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_call_parser_with_arguments.rpyc')))[1]

    assert type(decompressed[0]) == Label
    assert type(decompressed[0].block[0]) == Call
    assert expected == str(decompressed[0].block[0])
