import renpy.ast

from .block import Element

TYPE = renpy.ast.Pass

def parse(obj) -> Element:
    return Element(type='pass', value='pass')
