import renpy.ast

from .block import Element

TYPE = renpy.ast.Default

def parse(obj) -> Element:
    return Element(type='default', value='default %s = %s' % (obj.varname, obj.code.source))
