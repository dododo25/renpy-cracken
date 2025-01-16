import renpy.sl2.slast

from .block import Container, Element

TYPE = renpy.sl2.slast.SLScreen

def parse(obj) -> Element:
    return Container(type='screen', value=prepare_value(obj), children=prepare_children(obj))

def prepare_value(obj):
    res = 'screen %s' % obj.name

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

def prepare_children(obj):
    res = []

    if obj.modal and obj.modal != 'False':
        res.append(Element(type='property', value='modal %s' % obj.modal))
    
    if obj.sensitive and obj.sensitive != 'True':
        res.append(Element(type='property', value='sensitive %s' % obj.sensitive))

    if obj.tag:
        res.append(Element(type='property', value='tag %s' % obj.tag))

    if obj.zorder and obj.zorder != '0':
        res.append(Element(type='property', value='zorder %s' % obj.zorder))

    if obj.variant and obj.variant != 'None':
        res.append(Element(type='property', value='variant %s' % obj.variant))

    if obj.layer and obj.layer != "'screens'":
        res.append(Element(type='property', value='layer %s' % obj.layer))

    return res + obj.children
