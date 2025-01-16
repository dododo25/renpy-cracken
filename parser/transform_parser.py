import renpy.ast

from .block import Container, Element

TYPE = renpy.ast.Transform

def parse(obj) -> Element:
    return Container(type='transform', value=prepare_value(obj), children=obj.atl.statements)

def prepare_value(obj):
    res = 'style %s' % obj.varname

    if obj.parameters:
        args = obj.parameters

        prepared = []

        if args.parameters:
            prepared += list(map(lambda pair: pair[0] + (('=' + pair[1]) if pair[1] else ''), args.parameters))

        if args.extrapos:
            prepared.append('*' + args.extrapos)

        if args.extrakw:
            prepared.append('**' + args.extrakw)

        res += '(%s)' % ', '.join(prepared)

    return res + ':'
