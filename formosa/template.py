import svgwrite

from xml.etree import ElementTree as et

from .models import Box, MapBox, District
from .meta import STYLEPATH, GMLPATH, NS, GROUPS


def create(output='template.svg', size=(2000, 2000), stylesheet=STYLEPATH):
    dwg = svgwrite.Drawing(output, size=size, debug=False)

    with open(stylesheet, 'r') as f:
        dwg.add(
            dwg.style(f.read())
        )

    Box.dwg = dwg
    # use static variable for singleton

    boxes = {
        name: MapBox(
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
