import renpy.ast

from .block import Element

TYPE = renpy.ast.With

def parse(obj) -> Element:
    return Element(type='with', value='with %s' % obj.expr)
