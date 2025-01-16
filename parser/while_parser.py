import renpy.ast

from .block import Container, Element

TYPE = renpy.ast.While

def parse(obj) -> Element:
    return Container(type='while', value='while %s:' % obj.condition, children=obj.block)
