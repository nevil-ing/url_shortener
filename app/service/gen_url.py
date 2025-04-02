

def base62_encode(num):
    """convert a deceimal number to base62 representation"""
    chars = string.digits + string.ascii_lowercase + string.ascii_uppercase
    base = len(chars)
    result = "" 

    while num > 0:
        result = chars[num % base] + result
        num //= base
    return result or "0"    