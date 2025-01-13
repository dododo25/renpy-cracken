import renpy.ast
import re

from .block import Container, Element

TYPE = renpy.ast.Python

def parse(obj) -> Element:
    return Container(type='python', value=prepare_value(obj), children=prepare_parts(obj))

def prepare_value(obj):
    res = 'python'

    if obj.hide:
        res += ' hide'

    m = re.match(r'store(\.(.+))?', obj.store)

    if m and m.group(1):
        res += ' in %s' % m.group(2)

    return res + ':'

def prepare_parts(obj):
    res = []

    for v in obj.code.source.split('\n'):
        res.append(Element(type='code', value=v))

    return res
