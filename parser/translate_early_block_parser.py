import renpy.ast

from .block import Container, Element

TYPE = renpy.ast.TranslateEarlyBlock

def parse(obj) -> Element:
    return Container(type='translate', value='translate %s python:' % (obj.language), children=obj.block)
