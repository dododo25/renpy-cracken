import renpy.ast
import mommy

from .block import Container, Element

TYPE = renpy.ast.Style

def parse(obj) -> Element:
    return Container(type='style', value=prepare_value(obj), children=prepare_children(obj))

def prepare_value(obj):
    res = 'style %s' % obj.style_name

    if obj.parent:
        res += ' is %s' % obj.parent

    if obj.clear:
        res += ' clear'

    if obj.take:
        res += ' take %s' % obj.take

    if obj.variant:
        res += ' variant %s' % obj.variant

    return res + ':'

def prepare_children(obj):
    res = []

    for k, v in obj.properties.items():
        res.append(Element(type='property', value='%s %s' % (k, mommy.clean(v))))

    return res
