"""
ClipTools clipboard manager and text processing tools
with a lines based GUI interface

Utility functions
"""

from collections.abc import Callable


def limit_text(text: str, length: int) -> str:
    """Limit the text to display in the GUI
    result will be like: 'start of text [...]'"""
    text = text.strip()
    text = text.replace("\n", " ")
    if len(text) <= length:
        result = text
    else:
        result = text[: length - 5] + "[...]"
    return result


def safe_action(text: str, action: Callable[[str], str]) -> str:
    """Apply an action on a text and suppress exceptions"""
    try:
        result = action(text)
    except Exception as exc:  # pylint: disable=broad-except
        result = "ERROR: {}".format(exc)
    return result
