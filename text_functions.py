"""ClipTools clipboard manager and text processing tools
with a lines based GUI interface

Constants, configurations and shared info
"""

import os

from config import STRING_LENTH

TRANSLATE_TO_EN = str.maketrans("éÉáÁűŰőŐúÚöÖüÜóÓíÍ'\"+!%/=()", ";:'\"\\|[{]}0)-_=+`~!@#$%^&*(")
TRANSLATE_TO_HUN = str.maketrans(";:'\"\\|[{]}0)-_=+`~!@#$%^&*(", "éÉáÁűŰőŐúÚöÖüÜóÓíÍ'\"+!%/=()")


def limit_text(text, length=STRING_LENTH):
    """Limit the text to display in the GUI
    result will be like: 'start of text [...]'"""
    text = text.strip()
    if len(text) <= length:
        result = text
    else:
        result = text[:STRING_LENTH-5] + "[...]"
    result = result.replace("\n", " ")
    return result


def safe_action(text, action):
    """Apply an action on a text and suppress exceptions"""
    try:
        result = action(text)
    except Exception as exc:
        result = "ERROR: {}".format(exc)
    return result


def identity(text):
    """Dummy function, return the same text"""
    return text

def accents_to_hun(text):
    """Correct accents if you forgot to change to Hungarian keyboard"""
    return text.translate(TRANSLATE_TO_HUN)

def accents_to_en(text):
    """Correct accents if you forgot to change to English keyboard"""
    return text.translate(TRANSLATE_TO_EN)

def filename_linux(text):
    """Represent filenames with Linux/Unix stile forward slashes"""
    return text.replace("\\", "/")

def filename_double(text):
    """Represent filenames with double back slashes"""
    return text.replace("\\", "\\\\")

def filename_content(text):
    """Get the context of a full filename given as text"""
    if not os.path.isfile(text):
        return "ERROR: not a file"
    with open(text) as f:
        return f.read()
