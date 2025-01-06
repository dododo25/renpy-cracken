import renpy.ast

from block import Container, Element

TYPE = renpy.ast.Image

def parse(obj) -> Element:
    if obj.atl:
        return Container(type='image', value='image %s:' % ' '.join(obj.imgname), elements=obj.atl.statements)
    else:
        return Element(type='image', value='image %s = %s' % (' '.join(obj.imgname), obj.code.source))
