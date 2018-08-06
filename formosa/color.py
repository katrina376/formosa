import csv


def color(color_csv, template_path='template.svg', output='output.svg'):
    color_lists = {}

    with open(color_csv, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            color = row['color']
            code = row['code']
            if color not in color_lists:
                color_lists.update({color: []})
            color_lists[color].append(code)

    with open(template_path, 'r') as f:
        template = f.read()

    for color, codes in color_lists.items():
        template = template.replace(
            '{{__{}__}}'.format(color),
            ', '.join(['polygon[code="{}"]'.format(c) for c in codes])
        )

    with open(output, 'w') as o:
        o.write(template)
