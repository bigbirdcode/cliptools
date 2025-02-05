"""
ClipTools clipboard manager and text processing tools
with a lines based GUI interface

Global fixtures for Pytest
"""

import pathlib

import pytest

from cliptools.modules import config


@pytest.fixture
def testconfig() -> config.Config:
    """Change configuration values for easier test writing"""
    partial_config = pathlib.Path(__file__).parent / "test_resources" / "test_config.yml"
    c = config.read_config(pathlib.Path(), config_file=partial_config)
    assert not isinstance(c, str), c
    return c
