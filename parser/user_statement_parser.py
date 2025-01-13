import renpy.ast
import re

from .block import Element

TYPE = renpy.ast.UserStatement

def parse(obj) -> Element:
    type = 'statement'

    parts = re.split(r'\s+', obj.line)

    if parts[0] == 'window':
        if parts[1] == 'show':
            type += '-show'
        elif parts[1] == 'hide':
            type += '-hide'
        elif parts[1] == 'auto':
            type += '-auto'

    return Element(type=type, value=obj.line)
