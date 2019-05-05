"""ClipTools clipboard manager and text processing tools
with a lines based GUI interface

Utility functions
"""

from config import STRING_LENTH


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
