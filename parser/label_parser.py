import renpy.ast

from .block import Container, Element

TYPE = renpy.ast.Label

def parse(obj) -> Element:
    value = 'label %s' % obj.name

    if obj.parameters:
        value += '(%s)' % ', '.join(obj.parameters)

    return Container(type='label', value=value + ':', elements=obj.block)
