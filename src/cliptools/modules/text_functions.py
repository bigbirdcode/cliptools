"""ClipTools clipboard manager and text processing tools
with a lines based GUI interface

Text processing functions used to change active text content

You can add new functions as you like.
Naming: <action_group_name>_<action_name>(text)

Note: using doctest to show the usage of all functions.
"""

import os

from .data_struct import register_function
from . import sanitize


TRANSLATE_TO_EN = str.maketrans("éÉáÁűŰőŐúÚöÖüÜóÓíÍ'\"+!%/=()", ";:'\"\\|[{]}0)-_=+`~!@#$%^&*(")
TRANSLATE_TO_HUN = str.maketrans(";:'\"\\|[{]}0)-_=+`~!@#$%^&*(", "éÉáÁűŰőŐúÚöÖüÜóÓíÍ'\"+!%/=()")


@register_function
def paste_paste(text):
    """Dummy function, return the same text

    >>> paste_paste('foo')
    'foo'
    """
    return text


@register_function
def case_upper(text):
    """Text in UPPERCASE

    >>> case_upper('foO')
    'FOO'
    """
    return text.upper()


@register_function
def case_lower(text):
    """Text in lowercase

    >>> case_lower('FOo')
    'foo'
    """
    return text.lower()


@register_function
def case_title(text):
    """Text in Title Case

    >>> case_title('foO BAr')
    'Foo Bar'
    """
    return text.title()


@register_function
def accents_to_hun(text):
    """Correct accents if you forgot to change to Hungarian keyboard
    Note: I use Hungarian 101 key and US keyboards in parallel. But
    several times I forgot to change ad I type some garbage. These
    functions help correct the texts. Expect ű and í as they are
    ambiguous.

    >>> accents_to_hun("M'r megint elfelejt[d0tt a v'lt's")
    'Már megint elfelejtődött a váltás'
    """
    return text.translate(TRANSLATE_TO_HUN)


@register_function
def accents_to_en(text):
    """Correct accents if you forgot to change to English keyboard
    Note: I use Hungarian 101 key and US keyboards in parallel. But
    several times I forgot to change ad I type some garbage. These
    functions help correct the texts. Expect ű and í as they are
    ambiguous.

    >>> accents_to_en('if ÜÜnameÜÜ óó ÁÜÜmainÜÜÁÉ')
    'if __name__ == "__main__":'
    """
    return text.translate(TRANSLATE_TO_EN)


@register_function
def accents_shave_marks(text):
    """Remove all diacritic marks
    From the book "Fluent Python" by Luciano Ramalho (O'Reilly, 2015)

    >>> accents_shave_marks('ÁRVÍZTŰRŐ TÜKÖRFÚRÓGÉP')
    'ARVIZTURO TUKORFUROGEP'
    >>> accents_shave_marks('árvíztűrő tükörfúrógép')
    'arvizturo tukorfurogep'
    """
    return sanitize.shave_marks(text)


@register_function
def accents_asciize(text):
    """Remove all unicode to be plain ascii
    so that you can safely used to avoid the special characters.
    Be careful, still only useful only in Latin content.
    From the book "Fluent Python" by Luciano Ramalho (O'Reilly, 2015)

    >>> accents_asciize('“Öt szép szűzlány őrült írót nyúz”')
    '"Ot szep szuzlany orult irot nyuz"'
    """
    return sanitize.asciize(text)


@register_function
def accents_dewinize(text):
    """Replace Win1252 symbols with ASCII chars or sequences
    needed when copying code parts from MS Office, like Word...
    From the book "Fluent Python" by Luciano Ramalho (O'Reilly, 2015)

    >>> accents_dewinize('“Stupid word • error inside™ ”')
    '"Stupid word - error inside(TM) "'
    """
    return sanitize.dewinize(text)


@register_function
def filename_linux(text):
    r"""Represent filenames with Linux/Unix stile forward slashes

    >>> filename_linux('c:\\my documents\\bigbird')
    'c:/my documents/bigbird'
    """
    return text.replace("\\", "/")


@register_function
def filename_win(text):
    r"""Represent filenames with Linux/Unix stile forward slashes

    >>> filename_win('c:/my documents/bigbird')
    'c:\\my documents\\bigbird'
    """
    return text.replace("/", "\\")


@register_function
def filename_double(text):
    r"""Represent filenames with double back slashes

    >>> filename_double('c:\\my documents\\bigbird')
    'c:\\\\my documents\\\\bigbird'
    """
    return text.replace("\\", "\\\\")


@register_function
def filename_content(text):
    r"""Get the context of a full filename given as text

    >>> filename_content('tests/test_resources/test_text.txt')
    'This is a test file.\n'
    """
    if not os.path.isfile(text):
        return "ERROR: not a file"
    with open(text) as f:
        return f.read()


@register_function
def split_semicolon(text):
    """Split lines by semicolon
    Useful to manage path in windows or email names

    >>> split_semicolon('Jean;Jane; John')
    'Jean\\nJane\\nJohn'
    """
    return text.replace("; ", "\n").replace(";", "\n")
