import renpy.ast

from .block import Element

TYPE = renpy.ast.Jump

def parse(obj) -> Element:
    return Element(type='jump', value='jump %s' % obj.target)
