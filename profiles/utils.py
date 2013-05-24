import string

BASE_LIST = string.digits + string.ascii_letters

def to_alphanumeric(n):
    """convert positive decimal integer n to a custom format by defining BASE_LIST"""

    base = len(BASE_LIST)

    try:
        n = int(n)
    except:
        return ""

    if n < 0:
        return ""

    s = ""
    while 1:
        r = n % base
        s = BASE_LIST[r] + s
        n = n // base
        if n == 0:
            break

    return s
