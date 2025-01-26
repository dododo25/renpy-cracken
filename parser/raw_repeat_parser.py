import renpy.atl

from .block import Element

TYPE = renpy.atl.RawRepeat

def parse(obj) -> Element:
    value = 'repeat'

    if obj.repeats:
        value += ' %s' % obj.repeats

    return Element(type='atl', value=value)
