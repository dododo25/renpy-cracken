import renpy.atl

from .block import Element

TYPE = renpy.atl.RawTime

def parse(obj) -> Element:
    value = 'time'

    if obj.time:
        value += ' %s' % obj.time

    return Element(type='atl', value=value)
