color_syntax = {
    'hex': '#{}',
    'rgb': 'rgb({})',
    'name': '{}',
}

def color(data, path, output, mode='name'):
    color_lists = {}

    for d in data:
        color = d['color']
        code = d['code']
        if color not in color_lists:
            color_lists.update({color: []})
        color_lists[color].append(code)

    with open(path, 'r') as f:
        template = f.read()

    style_syntax = '{polygons} {{ fill: {color}; }}'
    mode = mode if mode in color_syntax else 'name'

    extensions = ' '.join([
        style_syntax.format(
            polygons=','.join(['polygon[code="{}"]'.format(c) for c in codes]),
            color=color_syntax[mode].format(color)
        )
        for color, codes in color_lists.items()
    ])

    template = template.replace('{{__EXTENSION__}}', extensions)

    with open(output, 'w') as o:
        o.write(template)
