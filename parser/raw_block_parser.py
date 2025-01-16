import renpy.atl

from .block import Container, Element

TYPE = renpy.atl.RawBlock

def parse(obj) -> Element:
    return Container(type='INVALID', children=obj.statements)
