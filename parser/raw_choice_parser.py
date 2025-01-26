import renpy.atl

from .block import Container, Element

TYPE = renpy.atl.RawChoice

def parse(obj) -> Element:
    return Container(type='atl', value='choice:', children=obj.choices)
