# Formosa

Generating SVG Taiwan maps and coloring them using Python 3.

## Features

1. generate an SVG template map using the district boundary datasets (`GML` or `SHP` files) provided by [NLSC](https://www.nlsc.gov.tw/)
2. render the template by specifying the district identification code and the color

## Requirements

- Python >= 3.6
- [svgwrite](https://pypi.org/project/svgwrite/)
- [pyshp](https://pypi.org/project/pyshp/)

## Data

1. download the ZIP files and unzip:
  - [鄉鎮市區界線(TWD97經緯度)](https://data.gov.tw/dataset/7441)
  - [直轄市、縣市界線(TWD97經緯度)](https://data.gov.tw/dataset/7442)
2. specify the paths to the unzipped `*.gml` files or `*.shp` files

## Examples

### Generate a map with default settings

```python
from formosa.template import create

output = 'template.svg'
boundary_fp = '/PATH/TO/FILE.shp'
template.create(output, boundary_fp)
```

### Generate a map with Penghu, Kinmen, and Matsu in floating boxes

```python
from formosa.template import create_from_obj

class Config:
    AREA_FILE_PATH = '/PATH/TO/AREA/FILE'
    BORDER_FILE_PATH = '/PATH/TO/BORDER/FILE'
    
    SIZE = (1040, 1040)
    
    ASSIGN_RULES = [
        (lambda name: '金門縣' in name, 'Kinmen'),
        (lambda name: '連江縣' in name, 'Matsu'),
        (lambda name: '澎湖縣' in name, 'Penghu'),
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
    }


output = 'template.svg'
create_from_obj(output, Config)
```

### Render a template

```python
from formosa.color import color

template = 'template.svg'

by_name = [{'code': '64000120', 'color': 'red'}]
by_hex = [{'code': '64000120', 'color': 'F00'}]
by_rgb = [{'code': '64000120', 'color': '255,0,0'}]

color(by_name, template, 'color_by_name.svg') # CSS color name
color(by_hex, template, 'color_by_hex.svg', 'hex')
color(by_rgb, template, 'color_by_rgb.svg', 'rgb')
```

### Render a template using Taiwan town codes ver.103

```python
from formosa.color import color
from formosa.utils.code import convert_TW103_to_MOI

template = 'template.svg'

data = [{'code': '6401200', 'color': 'red'}] # ver.103
for d in data:
    d.update({'code': convert_TW103_to_MOI(d.pop('code'))})

color(data, template, 'color_ver103_by_name.svg')
```
