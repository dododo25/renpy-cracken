import renpy.atl

from .block import Element

TYPE = renpy.atl.RawMultipurpose

def parse(obj) -> Element:
    if obj.expressions:
        return Element(type='atl', value='contains %s' % obj.expressions[0][0])

    if obj.properties:
        return Element(type='atl', value=' '.join(obj.properties[0]))

    return None
