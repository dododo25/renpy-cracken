import renpy.ast

from .block import Element

TYPE = renpy.ast.EndTranslate

def parse(_) -> Element:
    return Element(type='INVALID')
