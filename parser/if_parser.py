import renpy.ast

from block import Container, Element

TYPE = renpy.ast.If

def parse(obj) -> Element:
    elements = []

    for i in range(len(obj.entries)):
        entry = obj.entries[i]

        if i == 0:
            elements.append(Container(type='if', value='if:', *entry))
        elif entry[0] == 'True':
            elements.append(Container(type='else', value='else:', *entry))
        else:
            elements.append(Container(type='elif', value='elif:', *entry))

    return Container(type='INVALID', elements=elements)
