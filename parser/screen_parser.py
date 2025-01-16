import renpy.ast

from .block import Container, Element

TYPE = renpy.ast.Screen

def parse(obj) -> Element:
    return Container(type='INVALID', children=[obj.screen])
