import renpy.ast

from .block import Container, Element

TYPE = renpy.ast.Camera

def parse(obj) -> Element:
    value = 'camera'

    if obj.layer:
        value += ' %s' % obj.layer

    if obj.at_list:
        value += ' at %s' % ', '.join(obj.at_list)

    if obj.atl:
        return Container(type='camera', value=value + ':', children=obj.atl.statements)

    return Element(type='camera', value=value)
