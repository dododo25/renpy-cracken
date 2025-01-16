import renpy.ast

from .block import Container, Element

TYPE = renpy.ast.ShowLayer

def parse(obj) -> Element:
    value = 'show layer %s' % obj.layer

    if obj.at_list:
        value += ' at %s' % ', '.join(obj.at_list)

    if obj.atl:
        return Container(type='show', value=value + ':', children=obj.atl.statements)

    return Element(type='show', value=value)
