import string

MAPPED_CHARS = string.ascii_letters + string.digits
MAPPED_CHARS_LENGTH = len(MAPPED_CHARS)


def number_to_string(number):
    number = abs(number)
    chars = []
    while number > 0:
        mod = number % MAPPED_CHARS_LENGTH
        chars.append(MAPPED_CHARS[mod])
        number = number // MAPPED_CHARS_LENGTH
    return "".join(chars)
