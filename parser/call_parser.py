import renpy.ast

from .block import Element

TYPE = renpy.ast.Call

def parse(obj) -> Element:
    value = 'call %s' % obj.label

    if obj.arguments:
        value += '(%s)' % ', '.join(obj.arguments)

    return Element(type='call', value=value)
