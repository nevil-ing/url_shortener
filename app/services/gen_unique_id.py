import string

def base62_encode(num):
    """convert a deceimal number to base62 representation"""
    chars = string.digits + string.ascii_lowercase + string.ascii_uppercase
    base = len(chars)
    result = "" 

    while num > 0:
        result = chars[num % base] + result
        num //= base
    return result or "0"    

    def base62_decode(encoded):
       """Convert a base62 string to decimal"""
       chars = string.digits + string.ascii_lowercase + string.ascii_uppercase
       base = len(chars)
       length = len(encoded)
       num = 0
    
       for i, char in enumerate(encoded):
           power = length - (i + 1)
           num += chars.index(char) * (base ** power)
    
       return num