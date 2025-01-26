import renpy.atl

from .block import Container, Element

TYPE = renpy.atl.RawBlock

def parse(obj) -> Element:
    if len(obj.statements) < 2:
        return Container(type='INVALID', children=obj.statements)

    return Container(type='atl', value='block:', children=obj.statements)
