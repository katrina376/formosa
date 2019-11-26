color_syntax = {
    'hex': '#{}',
    'rgb': 'rgb({})',
    'name': '{}',
}

def color(data, path, output, mode='name', options={}):
    color_lists = {}

    for d in data:
        color = d['color']
        code = d['code']
        if color not in color_lists:
            color_lists.update({color: []})
        color_lists[color].append(code)

    with open(path, 'r') as f:
        template = f.read()

    style_syntax = '{selectors} {{ fill: {color}; }}'
    mode = mode if mode in color_syntax else 'name'
    
    extended_types = options.pop('extended_types', [])
    
    if not (isinstance(extended_types, list) or isinstance(extended_types, tuple)):
        raise TypeError('`extended_types` of `options` should be a list or a tuple.')
    
    all_types = ['.area', *extended_types]
    
    style = ''
    
    for t in all_types:
        if not isinstance(t, str):
            raise TypeError('Element type "{}" should be a string instead of "{}".'.format(str(t), type(t)))
        
        style += ' '.join([
            style_syntax.format(
                selectors=','.join(['{}[code="{}"]'.format(t, c) for c in codes]),
                color=color_syntax[mode].format(color)
            )
            for color, codes in color_lists.items()
        ])
    
    template = template.replace('#__extension_anchor {}', style)
    
    replace = options.pop('replace', [])
    
    for tp in replace:
        if not (isinstance(tp, list) or isinstance(tp, tuple)):
            raise TypeError('Elements from `replace` of `option` should be a list or a tuple.')
        
        if len(tp) != 2:
            raise ValueError('Elements from `replace` of `option` should be composed of 2 components.')
        
        target, text = tp
        template = template.replace(target, text)

    with open(output, 'w') as o:
        o.write(template)
