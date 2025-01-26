import renpy.atl

from .block import Element

TYPE = renpy.atl.RawContainsExpr

def parse(obj) -> Element:
    return Element(type='atl', value='contains %s' % obj.expression)
