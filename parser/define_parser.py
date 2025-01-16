import mommy
import renpy.ast
import re

from .block import Element

TYPE = renpy.ast.Define

def parse(obj) -> Element:
    value = 'define '

    m = re.match(r'store\.(.+)', obj.store)

    if m:
        value += m.group(1) + '.'

    value += '%s %s %s' % (obj.varname, obj.operator, mommy.clean(obj.code.source))

    return Element(type='define', value=value)
