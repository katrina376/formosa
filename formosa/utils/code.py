def convert_TW106_to_MOI(code):
    if not isinstance(code, str):
        raise TypeError('`code` should be a str.')
    
    if code[0] in ('0', '1'):
        return f'{code}0'
    elif code[0] == '6':
        return f'{code[0:2]}00{code[2:6]}'


def convert_TW103_to_MOI(code):
    return convert_TW106_to_MOI(code)


def convert_TW100_to_TW103(code):
    if not isinstance(code, str):
        raise TypeError('`code` should be a str.')
    
    if code[:5] == '10003':
        return f'680{code[5:]}0'
    else:
        return code


def convert_TW100_to_MOI(code):
    return convert_TW103_to_MOI(convert_TW100_to_TW103(code))
