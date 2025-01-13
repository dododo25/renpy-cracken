import renpy.ast

from .block import Container, Element

TYPE = renpy.ast.Label

def parse(obj) -> Element:
    value = 'label %s' % obj.name

    if obj.parameters:
        args = obj.parameters

        prepared = []

        if args.parameters:
            prepared += list(map(lambda pair: pair[0] + (('=' + pair[1]) if pair[1] else ''), args.parameters))

        if args.extrapos:
            prepared.append('*' + args.extrapos)

        if args.extrakw:
            prepared.append('**' + args.extrakw)

        value += '(%s)' % ', '.join(prepared)

    if obj.hide:
        value += ' hide'

    return Container(type='label', value=value + ':', children=obj.block)
