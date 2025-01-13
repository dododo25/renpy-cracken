import renpy.ast

from .block import Container, Element

TYPE = renpy.ast.Scene

def parse(obj) -> Element:
    value = 'scene'

    if obj.imspec:
        if obj.imspec[1]:
            value += ' expression %s' % obj.imspec[1]
        elif obj.imspec[0]:
            value += ' %s' % ' '.join(obj.imspec[0])

        if obj.imspec[2]:
            value += ' as %s' % obj.imspec[2]

        if obj.imspec[3]:
            value += ' at %s' % ' '.join(obj.imspec[3])

    if obj.atl:
        return Container(type='scene', value=value + ':', children=[obj.atl])

    return Element(type='scene', value=value)
