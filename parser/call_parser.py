import renpy.ast

from .block import Element

TYPE = renpy.ast.Call

def parse(obj) -> Element:
    value = 'call %s' % obj.label

    if obj.arguments:
        args = obj.arguments

        prepared = []

        if args.arguments:
            prepared += list(map(lambda pair: ((pair[0] + '=') if pair[0] else '') + pair[1], args.arguments))

        if args.extrapos:
            prepared.append('*' + args.extrapos)

        if args.extrakw:
            prepared.append('**' + args.extrakw)

        value += '(%s)' % ', '.join(prepared)

    return Element(type='call', value=value)
