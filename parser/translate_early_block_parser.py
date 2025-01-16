import renpy.ast

from .block import Container, Element

TYPE = renpy.ast.TranslateEarlyBlock

def parse(obj) -> Element:
    child = obj.block[0]

    if type(child) == renpy.ast.Style:
        elements = []

        for k, v in child.properties.items():
            elements.append(Element(type='style', value='%s %s' % (k, v)))

        return Container(type='translate', value='translate %s style %s:' % (obj.language, child.style_name), children=elements)

    return Container(type='translate', value='translate %s python:' % (obj.language), children=obj.block)
