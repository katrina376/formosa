color_syntax = {
    'hex': '#{}',
    'rgb': 'rgb({})',
    'name': '{}',
}

def color(data, path, output, mode='name', **options):
    color_lists = {}

    for d in data:
        if isinstance(d, dict):
            color = d.get('color')
            code = d.get('code')
        elif (isinstance(d, tuple) or isinstance(d, list)) and len(d) == 2:
            code, color = d
        else:
            raise ValueError('Elements in data should be a dict, a list, or a tuple.')
        
        if color not in color_lists:
            color_lists.update({color: set()})
        color_lists[color].add(code)

    with open(path, 'r') as f:
        template = f.read()

    style_syntax = '{selectors} {{ fill: {color}; }}'
    mode = mode if mode in color_syntax else 'name'
    
    extended = options.pop('extended_types', [])
    
    if not (isinstance(extended, list) or isinstance(extended, tuple)):
        raise TypeError('`extended` of `options` should be a list or a tuple.')
    
    all_types = ['.area', *extended]
    
    style = ''
    
    for type_ in all_types:
        if not isinstance(type_, str):
            raise TypeError(f'Element type "{type_}" should be a str')
        
        style += ' '.join([
            style_syntax.format(
                selectors=','.join([f'{type_}[code="{c}"]' for c in codes]),
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
