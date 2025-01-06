import renpy.ast

from .block import Element

TYPE = renpy.ast.Return

def parse(obj) -> Element:
    value = 'return'

    if obj.expression:
        value += ' %s' % obj.expression

    return Element(type='return', value=value)
