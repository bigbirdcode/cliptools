"""ClipTools clipboard manager and text processing tools
with a lines based GUI interface

Utility functions
"""

from cliptools import config


def limit_text(text, length=None):
    """Limit the text to display in the GUI
    result will be like: 'start of text [...]'"""
    if length is None:
        length = config.STRING_LENTH
    text = text.strip()
    text = text.replace("\n", " ")
    if len(text) <= length:
        result = text
    else:
        result = text[: length - 5] + "[...]"
    return result


def safe_action(text, action):
    """Apply an action on a text and suppress exceptions"""
    try:
        result = action(text)
    except Exception as exc:  # pylint: disable=broad-except
        result = "ERROR: {}".format(exc)
    return result
