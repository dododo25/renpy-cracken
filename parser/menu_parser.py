import renpy.ast

from block import Container, Element

TYPE = renpy.ast.Menu

def parse(obj) -> Element:
    value = 'menu'

    if obj.set:
        value += ', '.join(obj.set)

    return Container(type='menu', value=value + ':', elements=prepare_elements(obj))

def prepare_elements(obj):
    res = []

    for item in obj.items:
        value = '"%s"' % item[0]

        if item[1] and item[1] != 'True':
            value += ' if %s' % item[1]

        res.append(Container(type='option', value=value + ':', elements=item[2]))

    return res