import renpy.ast

from block import Element

TYPE = renpy.ast.UserStatement

def parse(obj) -> Element:
    type = 'statement'

    if obj.parsed[0] and obj.parsed[0][0] == 'window':
        if obj.parsed[0][1] == 'show':
            type += '-show'
        elif obj.parsed[0][1] == 'hide':
            type += '-hide'

    return Element(type=type, value=obj.line)
