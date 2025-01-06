import renpy.ast

from .block import Element

TYPE = renpy.ast.Hide

def parse(obj) -> Element:
    return Element(type='hide', value='hide %s' % ' '.join(obj.imspec[0]))
