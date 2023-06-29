import re

def turn_to_regexp(locale):
    if locale == 'en':
        return "([Tt]urn[ing]*\s+to\s+)(\d+)"
    if locale == 'fr':
        return "([\s\(]au\s+)(\d+)"
    raise ValueError(f'Unrecognized locale: "{locale}"')

def find_numbers(txt, locale):
    numbers = []
    for m in re.finditer(turn_to_regexp(locale), txt):
        turn_to = m.group(1)
        number = m.group(2)
        numbers.append(number)
    return numbers

