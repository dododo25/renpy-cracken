import renpy.ast

from .block import Container, Element

TYPE = renpy.ast.TranslateBlock

def parse(obj) -> Element:
    child = obj.block[0]
    return Container(type='translate', value='translate %s style %s:' % (obj.language, child.style_name), children=prepare_children(child))

def prepare_children(style):
    res = []

    for k, v in style.properties.items():
        res.append(Element(type='property', value='%s %s' % (k, v)))

    return res
