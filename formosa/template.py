import svgwrite

from xml.etree import ElementTree as et

from .models import Box, MapBox, District
from .meta import STYLEPATH, NS, GROUPS


def create(output, area, border=None, size=(2000, 2000), stylesheet=STYLEPATH, groups=GROUPS):
    if border is None:
        border = area
    
    dwg = svgwrite.Drawing(output, size=size, profile='tiny', debug=False)

    with open(stylesheet, 'r') as f:
        dwg.add(dwg.style(f.read() + '{{__EXTENSION__}}'))

    Box.dwg = dwg
    # use static variable for singleton

    boxes = {
        name: MapBox(
            name,
            **{k:v for k, v in group.items()})
        for name, group in groups.items()
    }

    area_coords = {}

    for ft in parse_features(area):
        dst = District(ft)
        for coord in dst.coordinates:
            boxes.get(dst.box_name).add_polygon(dst.code, coord, 'area')
            area_coords.update({coord: dst.box_name})

    for ft in parse_features(border):
        dst = District(ft)
        for coord in dst.coordinates:
            reassign_box_name = area_coords.get(coord, dst.box_name)
            # specialization for Ludao and Lanyu;
            # if the coords of the border of those two island,
            # go to the island's box;
            # else, stick to the original assign rule
            boxes.get(reassign_box_name).add_polygon(dst.code, coord, 'border')

    dwg.save()


def parse_features(path):
    tree = et.parse(path)
    root = tree.getroot()

    return root.findall('gml:featureMember', NS)
