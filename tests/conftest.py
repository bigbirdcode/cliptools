"""
ClipTools clipboard manager and text processing tools
with a lines based GUI interface

Global fixtures for Pytest
"""

import pathlib

import pytest

from cliptools.modules import config


@pytest.fixture
def test_resources() -> pathlib.Path:
    """Provides the resources folder in the tests."""
    return pathlib.Path(__file__).parent / "test_resources"


@pytest.fixture
def src_samples() -> pathlib.Path:
    """Provides the samples folder packed with sources."""
    return pathlib.Path(__file__).parent.parent / "src" / "cliptools" / "samples"


@pytest.fixture
def test_config(test_resources) -> config.Config:
    """
    Configuration values for easier test writing.

    You need to call 'sut.set_config(test_config)'
    """
    config_file = test_resources / "test_config.yml"
    c = config.read_config(pathlib.Path(), config_file=config_file)
    assert not isinstance(c, str), c
    return c
