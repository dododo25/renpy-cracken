import renpy.atl

from .block import Container, Element

TYPE = renpy.atl.RawOn

def parse(obj) -> Element:
    key, handler = list(obj.handlers.items())[0]
    return Container(type='on', value='on "%s" action:' % key, children=handler.statements)
