from .meta import NS, ASSIGN_RULES


class District:
    def __init__(self, node):
        region = node.find('pub:PUB_行政區域', NS)

        self.code = region.find('pub:行政區域代碼', NS).text
        self.name = region.find('pub:名稱', NS).text

        self.box_name = (
            [key for func, key in ASSIGN_RULES if func(self.name)] + ['main']
        )[0]

        area = region.find('pub:涵蓋範圍', NS)
        members = area.findall('gml:MultiPolygon/gml:polygonMember', NS)

        self.coordinates = [
            m.find(
                'gml:Polygon/gml:outerBoundaryIs/gml:LinearRing/gml:coordinates',
                NS,
            ).text
            for m in members
        ]


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
            self._scale(*p.split(','))
            for idx, p in enumerate(coordinates.split(' '))
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

        nx = (float(x) - xmin) * s
        ny = height + (- float(y) + ymin) * s

        return nx, ny

    def _remap(self, points):
        fx, fy = points[0]
        npoints = [(round(fx,1), round(fy,1))]

        for idx in range(1, len(points)):
            px, py = npoints[-1]
            x, y = points[idx]
            if round(px,1) != round(x,1) or round(py,1) != round(y,1):
                npoints.append((round(x,1), round(y,1)))

        return npoints
