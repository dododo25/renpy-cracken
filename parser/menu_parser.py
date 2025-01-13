import renpy.ast

from .block import Container, Element

TYPE = renpy.ast.Menu

def parse(obj) -> Element:
    return Container(type='menu', value='menu:', children=prepare_elements(obj))

def prepare_elements(obj):
    res = []

    if obj.set:
        res.append(Element(type='menuset', value='set %s' % obj.set))

    for item in obj.items:
        value = '"%s"' % item[0]

        if item[1] and item[1] != 'True':
            value += ' if %s' % item[1]

        res.append(Container(type='option', value=value + ':', children=item[2]))

    return res