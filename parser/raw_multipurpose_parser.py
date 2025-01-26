import renpy.atl

from .block import Container, Element

TYPE = renpy.atl.RawMultipurpose

def parse(obj) -> Element:
    if obj.warper or obj.warp_function:
        value = None

        if obj.warper:
            value = '%s %s' % (obj.warper, obj.duration)
        else:
            value = 'warp %s %s' % (obj.warp_function, obj.duration)

        if obj.splines:
            value += ''.join(map(lambda item: ' %s %s knot %s' % (item[0], item[1][-1], ' knot '.join(item[1][:-1])), obj.splines))

        if obj.expressions:
            value += ' ' + ' '.join(map(lambda item: item[0] + (' ' + item[1] if item[1] is not None else ''), obj.expressions))

        if obj.properties:
            value += ' ' + ' '.join(map(lambda item: ' '.join(item), obj.properties))

        if obj.revolution:
            value += ' ' + obj.revolution

        if obj.circles and obj.circles != '0':
            value += ' circles %s' % obj.circles

        return Element(type='atl', value=value)

    if obj.expressions or obj.properties:
        return Container(type='atl', value='contains:', children=prepare_children(obj.expressions + obj.properties))

    return None

def prepare_children(expr):
    res = []

    for k, v in expr:
        value = k

        if v:
            value += ' %s' % v

        res.append(Element(type='atl', value=value))

    return res
