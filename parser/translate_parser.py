import renpy.ast

from .block import Container, Element

TYPE = renpy.ast.Translate

def parse(obj) -> Element:
    return Container(type='translate', value='translate %s %s:' % (obj.language, obj.identifier), children=obj.block)
