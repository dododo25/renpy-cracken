import renpy.sl2.slast

from .block import Element

TYPE = renpy.sl2.slast.SLDisplayable

def parse(obj) -> Element:
    return Element(type='INVALID')
