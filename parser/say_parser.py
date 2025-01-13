import renpy.ast

from .block import Element

TYPE = renpy.ast.Say

def parse(obj) -> Element:
    value = ''

    if obj.who:
        value += '%s ' % obj.who

    if obj.attributes:
        value += '%s ' % ', '.join(obj.attributes)

    value += '"%s"' % obj.what

    if obj.arguments:
        args = obj.arguments

        prepared = []

        if args.arguments:
            prepared += list(map(lambda pair: ((pair[0] + '=') if pair[0] else '') + pair[1], args.arguments))

        if args.extrapos:
            prepared.append('*' + args.extrapos)

        if args.extrakw:
            prepared.append('**' + args.extrakw)
        
        value += ' (%s)' % ', '.join(prepared)

    if obj.with_:
        value += ' with %s' % obj.with_

    return Element(type='say', value=value)
