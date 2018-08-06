import os


ASSET_ROOT = os.path.join(os.path.dirname(__file__), 'assets')

GMLFILES = {
    'county': 'COUNTY_MOI_1060503',
    'town': 'TOWN_MOI_1060503',
}

GMLPATH = {
    k: os.path.join(ASSET_ROOT, n + '.gml') for k, n in GMLFILES.items()}

STYLEPATH = os.path.join(ASSET_ROOT, 'stylesheet.css')

NS = {
    'pub': 'http://standards.moi.gov.tw/schema/pub',
    'gml': 'http://www.opengis.net/gml',
}

FILTERS = [
    (lambda name: '金門縣' in name, 'Kinmen'),
    (lambda name: '連江縣' in name, 'Matsu'),
    (lambda name: '澎湖縣' in name, 'Penghu'),
    (lambda name: '綠島' in name, 'Ludao'),
    (lambda name: '蘭嶼' in name, 'Lanyu'),
]

GROUPS = {
    'main': {
        'position': (0, 0),
        'size': (1, 1),
        'border': (118.6, 120.6, 21.7, 25.5),
        'skip': 16,
    },
    'Penghu': {
        'position': (0.02, 0.55),
        'size': (0.3, 0.225),
        'border': (119.38, 119.5, 23.4, 23.7),
        'skip': 4,
    },
    'Kinmen': {
        'position': (0.02, 0.285),
        'size': (0.3, 0.225),
        'border': (118, 118.5, 24.25, 24.4),
        'skip': 4,
    },
    'Matsu': {
        'position': (0.02, 0.02),
        'size': (0.3, 0.225),
        'border': (119.8, 119.95, 26.1, 26.3),
        'skip': 4,
    },
    'Ludao': {
        'position': (0.78, 0.64),
        'size': (0.2, 0.15),
        'border': (121.45, 121.52, 22.61, 22.69),
        'skip': 4,
    },
    'Lanyu': {
        'position': (0.78, 0.83),
        'size': (0.2, 0.15),
        'border': (121.49, 121.62, 21.94, 22.09),
        'skip': 4,
    },
}

# Kinmen
# (118.14367476000007, 119.47920615500004, 24.16025806600004, 24.999616759000048)
# main
# (119.99689695800005, 124.56114950000006, 21.895599675000085, 25.92913772500009)
# Ludao
# (121.46433504200002, 121.512131544, 22.631834368000057, 22.68170751200006)
# Lanyu
# (121.49934627000005, 121.61640099600004, 21.942511678000074, 22.08784228500008)
# Matsu
# (119.908897282, 120.51174267100009, 25.940998015000048, 26.385278130000074)
# Penghu
# (119.31429438700002, 119.72756791000006, 23.186564029000067, 23.810694694000063)
