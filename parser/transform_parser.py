import renpy.ast

from .block import Container, Element

TYPE = renpy.ast.Transform

def parse(obj) -> Element:
    return Container(type='transform', value=prepare_value(obj), children=obj.atl.statements)

def prepare_value(obj):
    res = 'transform %s' % obj.varname

    if obj.parameters:
        prepared = []

        for p in obj.parameters.parameters.values():
            v = p.name

            if p.default is not None:
                v += '=' + p.default

            prepared.append(v)

        res += '(%s)' % ', '.join(prepared)

    return res + ':'
