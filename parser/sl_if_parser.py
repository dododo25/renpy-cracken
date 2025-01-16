import renpy.sl2.slast

from .block import Container, Element

TYPE = renpy.sl2.slast.SLIf

def parse(obj) -> Element:
    children = []

    for i, entry in enumerate(obj.entries):
        if i == 0:
            children.append(Container(type='if', value='if %s:' % entry[0], children=entry[1].children))
        elif entry[0] is None or entry[0] == 'True':
            children.append(Container(type='else', value='else:', children=entry[1].children))
        else:
            children.append(Container(type='elif', value='elif %s:' % entry[0], children=entry[1].children))

    return Container(type='INVALID', children=children)
