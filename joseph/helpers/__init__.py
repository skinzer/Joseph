import re

from .stack import Stack

# Regexes taken from http://stackoverflow.com/questions/1175208/elegant-python-function-to-convert-camelcase-to-snake-case
first_cap_re = re.compile('(.)([A-Z][a-z]+)')
all_cap_re = re.compile('([a-z0-9])([A-Z])')

def camel_to_snake(name):
    s1 = first_cap_re.sub(r'\1_\2', name)
    return all_cap_re.sub(r'\1_\2', s1).lower()

def coroutine(func):
    """
    Simple decorator to prime a coroutine
    """
    def wrap(*args, **kwargs):
        cr = func(*args, **kwargs)
        cr.next()
        return cr
    return wrap
