"""
ClipTools clipboard manager and text processing tools
with a lines based GUI interface

Test

Config file reading test
"""

# ruff: noqa: D103 - missing docstring

import pathlib

from cliptools.modules import config


def test_partial_config_can_be_read_with_values(test_resources):
    partial_config = test_resources / "config_partial.yml"
    c = config.read_config(pathlib.Path(), config_file=partial_config)
    assert not isinstance(c, str), c
    assert c.port == 9999
    assert c.number_of_rows == 1
    assert c.string_length == 30  # default


def test_cannot_read_wrong_config(test_resources):
    wrong_config = test_resources / "config_wrong.yml"
    c = config.read_config(pathlib.Path(), config_file=wrong_config)
    assert isinstance(c, str), "No error reported"
    assert "unexpected key not in schema" in c, f"Wrong error in {c}"
