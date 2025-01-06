import renpy.ast

from .block import Element

TYPE = renpy.ast.Scene

def parse(obj) -> Element:
    return Element(type='scene', value='scene %s' % ' '.join(obj.imspec[0]))
