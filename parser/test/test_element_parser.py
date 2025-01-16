from parser.block import Element
from parser.element_parser import parse

def test_parse_element_statement():
    expected = input = Element(type='any', value='any')
    assert expected == parse(input)
