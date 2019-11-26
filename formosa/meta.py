import os


ASSET_ROOT = os.path.join(os.path.dirname(__file__), 'assets')

STYLEPATH = os.path.join(ASSET_ROOT, 'stylesheet.css')

NS = {
    'pub': 'http://standards.moi.gov.tw/schema/pub',
    'gml': 'http://www.opengis.net/gml',
}

ASSIGN_RULES = [
    (lambda name: '金門縣' in name, 'Kinmen'),
    (lambda name: '連江縣' in name, 'Matsu'),
    (lambda name: '澎湖縣' in name, 'Penghu'),
    (lambda name: '綠島' in name, 'Ludao'),
    (lambda name: '蘭嶼' in name, 'Lanyu'),
]

GROUPS = {
    'main': {
        'display_name': '',
        'position': (0, 0),
        'size': (1, 1),
        'border': (118.6, 120.6, 21.7, 25.5),
        'skip': 16,
    },
    'Penghu': {
        'display_name': '澎湖',
        'position': (0.02, 0.5),
        'size': (0.32, 0.48),
        'border': (119.3, 119.35, 23.14, 23.82),
        'skip': 4,
    },
    'Kinmen': {
        'display_name': '金門',
        'position': (0.02, 0.26),
        'size': (0.32, 0.2),
        'border': (118.1, 118.6, 24.28, 24.42),
        'skip': 4,
    },
    'Matsu': {
        'display_name': '連江',
        'position': (0.02, 0.02),
        'size': (0.32, 0.2),
        'border': (119.81, 120.01, 26.1, 26.3),
        'skip': 4,
    },
    'Ludao': {
        'display_name': '綠島',
        'position': (0.78, 0.64),
        'size': (0.2, 0.15),
        'border': (121.4, 121.48, 22.57, 22.76),
        'skip': 4,
    },
    'Lanyu': {
        'display_name': '蘭嶼',
        'position': (0.78, 0.83),
        'size': (0.2, 0.15),
        'border': (121.47, 121.55, 21.96, 22.15),
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
