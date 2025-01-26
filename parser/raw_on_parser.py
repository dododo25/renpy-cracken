import renpy.atl

from .block import Container, Element

TYPE = renpy.atl.RawOn

def parse(obj) -> Element:
    return Container(type='atl', value='on %s:' % ', '.join(obj.handlers.keys()), children=list(obj.handlers.values())[0].statements)
