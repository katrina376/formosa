from formosa import template
from formosa.color import color


# Create template map
template.create('test.svg')

# Color the template map using the list of districts
color('demo/test.csv', 'test.svg', 'test_color.svg')
