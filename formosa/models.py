from xml.etree import ElementTree as et

import shapefile

from .meta import NS


class ProcessFileError(Exception):
    def __init__(self, fp):
        message = f'Cannot process file as GML or SHP: {fp}'
        super(Exception, self).__init__(message)


class District:
    @classmethod
    def from_file(cls, fp, assign_rules=[]):
        try:
            tree = et.parse(fp)
            return cls.from_gml(fp, assign_rules)
        except et.ParseError:
            pass
        
        try:
            with shapefile.Reader(fp):
                return cls.from_shp(fp, assign_rules)
        except:
            raise ProcessFileError(fp)
        
    @classmethod
    def from_gml(cls, fp, assign_rules=[]):
        tree = et.parse(fp)
        root = tree.getroot()
        nodes = root.findall('gml:featureMember', NS)
        
        for node in nodes:
            region = node.find('pub:PUB_行政區域', NS)

            code = region.find('pub:行政區域代碼', NS).text
            name = region.find('pub:名稱', NS).text

            area = region.find('pub:涵蓋範圍', NS)
            members = [
                m.find(
                    'gml:Polygon/gml:outerBoundaryIs/gml:LinearRing/gml:coordinates',
                    NS,
                ).text
                for m in area.findall('gml:MultiPolygon/gml:polygonMember', NS)
            ]
            
            coordinates = [
                tuple(
                    tuple(float(s) for s in coor.split(','))
                    for coor in line.split(' ')
                )
                for line in members
            ]
            
            yield cls(code, name, coordinates, assign_rules)
    
    @classmethod
    def from_shp(cls, fp, assign_rules=[]):
        with shapefile.Reader(fp) as sf:
            srs = sf.shapeRecords()

        for s in srs:
            if hasattr(s.record, 'TOWNCODE'):
                code = s.record.TOWNCODE
                name = f'{s.record.COUNTYNAME}{s.record.TOWNNAME}'
            else:
                code = s.record.COUNTYCODE
                name = s.record.COUNTYNAME

            coordinates = []

            for idx, start in enumerate(s.shape.parts):
                end = s.shape.parts[idx + 1] if idx + 1 < len(s.shape.parts) else None
                coordinates.append(tuple(s.shape.points[start:end]))

            yield cls(code, name, coordinates, assign_rules)
    
    def __init__(self, code, name, coordinates, assign_rules=[]):
        self.code = code
        self.name = name
        self.coordinates = coordinates
        
        self.box_name = (
            [key for func, key in assign_rules if func(self.name)] + ['main']
        )[0]
        

class Box:
    dwg = None

    def __init__(self, name, position, size):
        if self.dwg is None:
            raise ValueError('`dwg` should be set.')

        if type(name) is not str:
            raise TypeError('`name` should be a string.')

        if type(position) is not tuple or len(position) != 2:
            raise TypeError('`position` should be a tuple with the length of 2.')

        if type(size) is not tuple or len(size) != 2:
            raise TypeError('`size` should be a tuple with the length of 2.')

        self.name = name

        self.size = (
            size[0] * self.dwg['width'],
            size[1] * self.dwg['height'],
        )
        self.position = (
            position[0] * self.dwg['width'],
            position[1] * self.dwg['height'],
        )

        self.g = self.dwg.g(
            id='group-' + name,
        )
        self.g.translate(*self.position)
        self.g.add(
            self.dwg.rect(
                size=self.size,
                id='rect-' + name,
                class_='mapbox-base'
            )
        )

        self.dwg.add(self.g)


class MapBox(Box):
    def __init__(self, name, position, size, border, skip, display_name):
        super(MapBox, self).__init__(name, position, size)

        if type(display_name) is not str:
            raise TypeError('`display_name` should be a string.')

        if type(position) is not tuple or len(position) != 2:
            raise TypeError('`position` should be a tuple with the length of 2.')

        if type(size) is not tuple or len(size) != 2:
            raise TypeError('`size` should be a tuple with the length of 2.')

        self.display_name = display_name

        self.border = border
        self.skip = skip

        self.clip = self.dwg.defs.add(
            self.dwg.clipPath(
                id='clip-' + name
            )
        )
        self.clip.add(self.dwg.rect(size=self.size))

        padding = self.dwg['width'] * 0.02
        self.g.add(
            self.dwg.text(
                self.display_name,
                insert=(self.size[0] - padding, self.size[1] - padding),
                text_anchor='end',
                class_='mapbox-name',
            )
        )

    def add_polygon(self, code, coordinates, kind):
        points = self._remap([
            self._scale(*p)
            for idx, p in enumerate(coordinates)
            if idx % self.skip == 0
        ])
        self.g.add(
            self.dwg.polygon(
                points,
                code=code,
                class_=kind,
                clip_path='url(#clip-{})'.format(self.name)
            )
        )

    def _scale(self, x, y):
        xmin, xmax, ymin, ymax = self.border
        width, height = self.size

        s = min(width / (xmax - xmin), height / (ymax - ymin))

        nx = (x - xmin) * s
        ny = height + (- y + ymin) * s

        return nx, ny

    def _remap(self, points):
        fx, fy = points[0]
        npoints = [(round(fx, 1), round(fy, 1))]

        for idx in range(1, len(points)):
            px, py = npoints[-1]
            x, y = points[idx]
            if round(px, 1) != round(x, 1) or round(py, 1) != round(y, 1):
                npoints.append((round(x, 1), round(y, 1)))

        return npoints
