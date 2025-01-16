import renpy.ast

from .block import Container, Element

TYPE = renpy.ast.TranslateString

def parse(obj) -> Element:
    elements = [
        Element(type='translate-old', value='old "%s"' % obj.old), 
        Element(type='translate-new', value='new "%s"' % obj.new)
    ]

    return Container(type='translate', value='translate %s strings:' % obj.language, children=elements)
