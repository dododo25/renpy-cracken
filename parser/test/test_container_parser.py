from parser.block import Container
from parser.container_parser import parse

def test_parse_container_statement():
    expected = input = Container(type='any', value='any')
    assert expected == parse(input)
