import renpy.ast

from .block import Container, Element

TYPE = renpy.ast.Init

def parse(obj) -> Element:
    value = 'init'

    if obj.priority:
        value += ' %s' % obj.priority

    return Container(type='init', value=value + ':', children=obj.block)
