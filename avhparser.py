import re

def default_locale_prefix(locale):
    if locale == 'en':
        return "([Tt]urn[ing]*\s+to\s+)"
    if locale == 'fr':
        return "([\s\(]au\s+)"
    raise ValueError(f'Unsupported locale: "{locale}"')

def prefix(kwargs):
    if "prefix" in kwargs and kwargs["prefix"]:
        return kwargs["prefix"]
    if "locale" in kwargs and kwargs["locale"]:
        return default_locale_prefix(kwargs["locale"])
    raise ValueError('Please provide a locale or an explicit prefix')

def find_numbers(txt, **kwargs):
    numbers = []
    regexp = prefix(kwargs) + "(\d+)"
    for m in re.finditer(regexp, txt):
        number = m.group(m.lastindex)
        numbers.append(number)
    return numbers

