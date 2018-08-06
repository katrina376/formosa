import svgwrite

from xml.etree import ElementTree as et

from .models import Box, District
from .meta import STYLEPATH, GMLPATH, NS, CANVAS, GROUPS


def create(output='template.svg', stylesheet=STYLEPATH):
    dwg = svgwrite.Drawing(output, size=CANVAS, debug=False)

    with open(stylesheet, 'r') as f:
        dwg.add(
            dwg.style(f.read())
        )

    Box.dwg = dwg
    # use static variable for singleton

    boxes = {
        name: Box(
            name,
            **{k:v for k, v in group.items()})
        for name, group in GROUPS.items()
    }

    boxes = _draw(boxes, GMLPATH.get('town'), 'town')
    boxes = _draw(boxes, GMLPATH.get('county'), 'county')

    dwg.save()


def _draw(boxes, path, kind):
    tree = et.parse(path)
    root = tree.getroot()

    features = root.findall('gml:featureMember', NS)

    for ft in features:
        dst = District(ft)
        for c in dst.coordinates:
            boxes.get(dst.box_name).add_polygon(dst.code, c, kind)

    return boxes
