import renpy.atl

from .block import Container, Element

TYPE = renpy.atl.RawChild

def parse(obj) -> Element:
    return Container(type='INVALID', children=obj.children)
