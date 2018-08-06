from .meta import NS, FILTERS


class District:
    def __init__(self, node):
        region = node.find('pub:PUB_行政區域', NS)

        self.code = region.find('pub:行政區域代碼', NS).text
        self.name = region.find('pub:名稱', NS).text

        self.box_name = (
            [key for func, key in FILTERS if func(self.name)] + ['main']
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

    def __init__(self, name, position, size, border, skip=4, reverse=False):
        if self.dwg is None:
            raise ValueError('`dwg` should be set.')

        if type(name) is not str:
            raise TypeError('`name` should be a string.')

        if type(position) is not tuple or len(position) != 2:
            raise TypeError('`position` should be a tuple with the length of 2.')

        if type(size) is not tuple or len(size) != 2:
            raise TypeError('`size` should be a tuple with the length of 2.')

        if type(border) is not tuple or len(border) != 4:
            raise TypeError('`border` should be a tuple with the length of 4.')

        self.name = name
        self.size = size
        self.border = border
        self.skip = skip

        self.reverse = reverse

        self.clip = self.dwg.defs.add(
            self.dwg.clipPath(
                id='clip-' + name
            )
        )
        self.clip.add(self.dwg.rect(size=size))

        self.g = self.dwg.g(
            id='group-' + name,
        )
        self.g.translate(*position)
        self.g.add(
            self.dwg.rect(
                size=size,
                id='rect-' + name,
                class_='base'
            )
        )
        self.dwg.add(self.g)

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
                clip_path='url(#{})'.format('clip-' + self.name)
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
        npoints = []

        for idx in range(len(points)-1):
            px, py = points[idx]
            x, y = points[idx+1]
            if round(px) != round(x) or round(py) != round(y):
                npoints.append(points[idx+1])

        return npoints
