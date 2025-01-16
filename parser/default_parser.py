import mommy
import renpy.ast
import re

from .block import Element

TYPE = renpy.ast.Default

def parse(obj) -> Element:
    value = 'default '

    m = re.match(r'store\.(.+)', obj.store)

    if m:
        value += m.group(1) + '.'

    value += '%s = %s' % (obj.varname, mommy.clean(obj.code.source))

    return Element(type='default', value=value)
