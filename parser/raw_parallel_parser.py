import renpy.atl

from .block import Container, Element

TYPE = renpy.atl.RawParallel

def parse(obj) -> Element:
    return Container(type='atl', value='parallel:', children=obj.blocks)
