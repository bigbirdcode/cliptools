"""ClipTools clipboard manager and text processing tools
with a lines based GUI interface

Text processing functions used to change active text content
"""

import os

from data_struct import register_function
import sanitize


TRANSLATE_TO_EN = str.maketrans("éÉáÁűŰőŐúÚöÖüÜóÓíÍ'\"+!%/=()", ";:'\"\\|[{]}0)-_=+`~!@#$%^&*(")
TRANSLATE_TO_HUN = str.maketrans(";:'\"\\|[{]}0)-_=+`~!@#$%^&*(", "éÉáÁűŰőŐúÚöÖüÜóÓíÍ'\"+!%/=()")


@register_function
def paste_paste(text):
    """Dummy function, return the same text"""
    return text


@register_function
def case_upper(text):
    """Text in UPPERCASE"""
    return text.upper()


@register_function
def case_lower(text):
    """Text in lowercase"""
    return text.lower()


@register_function
def case_title(text):
    """Text in Title Case"""
    return text.title()


@register_function
def accents_to_hun(text):
    """Correct accents if you forgot to change to Hungarian keyboard"""
    return text.translate(TRANSLATE_TO_HUN)


@register_function
def accents_to_en(text):
    """Correct accents if you forgot to change to English keyboard"""
    return text.translate(TRANSLATE_TO_EN)


@register_function
def accents_shave_marks(text):
    """Remove all diacritic marks"""
    return sanitize.shave_marks(text)


@register_function
def accents_asciize(text):
    """Remove all unicode to be plain ascii"""
    return sanitize.asciize(text)


@register_function
def accents_dewinize(text):
    """Replace Win1252 symbols with ASCII chars or sequences"""
    return sanitize.dewinize(text)


@register_function
def filename_linux(text):
    """Represent filenames with Linux/Unix stile forward slashes"""
    return text.replace("\\", "/")


@register_function
def filename_double(text):
    """Represent filenames with double back slashes"""
    return text.replace("\\", "\\\\")


@register_function
def filename_content(text):
    """Get the context of a full filename given as text"""
    if not os.path.isfile(text):
        return "ERROR: not a file"
    with open(text) as f:
        return f.read()


@register_function
def split_semicolon(text):
    """Split lines by semicolon"""
    return text.replace(";", "\n")
