import renpy.atl

from .block import Element

TYPE = renpy.atl.RawFunction

def parse(obj) -> Element:
    value = 'function'

    if obj.expr:
        value += ' %s' % obj.expr

    return Element(type='atl', value=value)
