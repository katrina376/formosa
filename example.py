import csv

from formosa import template
from formosa.color import color


template_name = 'test.svg'

# Create template map
template.create(template_name, (1040, 1040))

# Color the template map using the list of districts
with open('demo/color_by_name.csv', 'r') as csvfile:
    data = [row for row in csv.DictReader(csvfile)]
    color(data, template_name, 'test_by_name.svg')

with open('demo/color_by_hex.csv', 'r') as csvfile:
    data = [row for row in csv.DictReader(csvfile)]
    color(data, template_name, 'test_by_hex.svg', 'hex')

with open('demo/color_by_rgb.csv', 'r') as csvfile:
    data = [row for row in csv.DictReader(csvfile)]
    color(data, template_name, 'test_by_rgb.svg', 'rgb')
