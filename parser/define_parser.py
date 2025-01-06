import renpy.ast

from .block import Element

TYPE = renpy.ast.Define

def parse(obj) -> Element:
    return Element(type='define', value='define %s %s %s' % (obj.varname, obj.operator, obj.code.source))
