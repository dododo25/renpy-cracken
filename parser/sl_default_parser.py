import renpy.sl2.slast

from .block import Element

TYPE = renpy.sl2.slast.SLDefault

def parse(obj) -> Element:
    return Element(type='default', value='default %s = %s' % (obj.variable, obj.expression))
