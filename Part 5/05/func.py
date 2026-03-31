def string_to_float(s):
    if not s:
        return None

    sign = 1
    if s[0] == '-':
        sign = -1
        s = s[1:]
    elif s[0] == '+':
        s = s[1:]

    if not s:
        return None

    if '.' in s:
        parts = s.split('.')
        if len(parts) != 2 or parts[0] == "" or parts[1] == "":
            return None
        int_part, frac_part = parts
    else:
        int_part = s
        frac_part = ""

    if not int_part.isdigit():
        return None
    if frac_part and not frac_part.isdigit():
        return None

    integer = 0
    for ch in int_part:
        integer = integer * 10 + (ord(ch) - ord('0'))

    fraction = 0
    divisor = 10
    for ch in frac_part:
        fraction += (ord(ch) - ord('0')) / divisor
        divisor *= 10

    return sign * (integer + fraction)
