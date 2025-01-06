import renpy.ast

from .block import Element

TYPE = renpy.ast.Show

def parse(obj) -> Element:
    return Element(type='show', value='show %s' % ' '.join(obj.imspec[0]))