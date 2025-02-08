"""
ClipTools clipboard manager and text processing tools
with a lines based GUI interface

Test

Utility functions
"""

# ruff: noqa: D103 - missing docstring

from cliptools.modules import utils


def action_good(text):
    return "good:" + text


def action_wrong(text):
    return str(1 / 0) + text


def test_limit_text_short():
    in_txt = "Short\ntext"
    ou_txt = "Short text"
    assert utils.limit_text(in_txt, 10) == ou_txt


def test_limit_text_long():
    in_txt = "Long\nand\nboring\ntext"
    ou_txt = "Long [...]"
    assert utils.limit_text(in_txt, 10) == ou_txt


def test_safe_action_good():
    assert utils.safe_action("good", action_good) == "good:good"


def test_safe_action_wrong():
    assert utils.safe_action("wrong", action_wrong) == "ERROR: division by zero"
