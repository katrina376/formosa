import svgwrite

import os.path

from .models import Box, MapBox, District
from .meta import STYLEPATH, GROUPS, ASSIGN_RULES


def create(output, area, border=None, size=(2000, 2000), **options):
    stylesheet = options.get('stylesheet', STYLEPATH)
    groups = options.get('groups', GROUPS)
    assign_rules = options.get('assign_rules', ASSIGN_RULES)
    
    if border is None:
        border = area
    
    if not os.path.isfile(area):
        raise FileNotFoundError(f'Area path is not a regular file: {area}')
    
    if not os.path.isfile(border):
        raise FileNotFoundError(f'Border path is not a regular file: {border}')
    
    dwg = svgwrite.Drawing(output, size=size, profile='tiny', debug=False)

    with open(stylesheet, 'r') as f:
        dwg.add(dwg.style(f.read() + '#__extension_anchor {}'))

    Box.dwg = dwg
    # use static variable for singleton

    boxes = {
        name: MapBox(
            name,
            **{k:v for k, v in group.items()})
        for name, group in groups.items()
    }

    area_coords = {}
    
    area_districts = District.from_file(area, assign_rules)
    
    for dst in area_districts:
        for coord in dst.coordinates:
            boxes.get(dst.box_name).add_polygon(dst.code, coord, 'area')
            area_coords.update({coord: dst.box_name})
    
    border_districts = District.from_file(border, assign_rules)
        
    for dst in border_districts:
        for coord in dst.coordinates:
            reassign_box_name = area_coords.get(coord, dst.box_name)
            # specialization for Ludao and Lanyu;
            # if the coords of the border of those two island,
            # go to the island's box;
            # else, stick to the original assign rule
            boxes.get(reassign_box_name).add_polygon(dst.code, coord, 'border')

    dwg.save()
