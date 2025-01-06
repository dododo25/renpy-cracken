import renpy.ast

from .block import Element

TYPE = renpy.ast.Say

def parse(obj) -> Element:
    value = ''

    if obj.who:
        value += "%s " % obj.who

    value += '"%s"' % obj.what

    if obj.with_:
        value += " with %s" % obj.with_

    return Element(type='say', value=value)
