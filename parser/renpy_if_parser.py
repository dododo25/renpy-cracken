import renpy

from block import EmptyLine, IfPart

TYPE = renpy.ast.If

def parse(obj, level):
    parts = [EmptyLine()]

    for i in range(len(obj.entries)):
        entry = obj.entries[i]

        if i == 0:
            parts.append(IfPart('if', *entry))
        elif entry[0] == 'True':
            parts.append(IfPart('else', *entry))
        else:
            parts.append(IfPart('elif', *entry))

    parts.append(EmptyLine())

    return None, level, parts
