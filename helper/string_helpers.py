import random
import re
import string
import uuid


def convert_camel_to_underscore(s):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', s)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def random_string_generator(size=9, chars=string.digits):
    return int("1" + ''.join(random.choice(chars) for _ in range(size)))


def remove_unsafe_html_elements(raw_html):
    if not isinstance(raw_html, str):
        return ""
    pattern = r"""<(script|iframe|embed|frame|frameset|object|applet|body|html|style|layer|link|ilayer|meta|bgsound)|((alert|on\w+|function\s+\w+)\s*\(\s*(['+\d\w](,?\s*['+\d\w]*)*)*\s*\))"""
    return re.sub(pattern, repl="", string=raw_html)


def hash_str_to_uuid(input_string):
    return str(uuid.uuid5(uuid.NAMESPACE_X500, input_string))
