import renpy.atl

from .block import Element

TYPE = renpy.atl.RawEvent

def parse(obj) -> Element:
    value = 'event'

    if obj.name:
        value += ' %s' % obj.name

    return Element(type='atl', value=value)
