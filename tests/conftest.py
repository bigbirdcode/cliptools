"""ClipTools clipboard manager and text processing tools
with a lines based GUI interface

Global fixtures for Pytest
"""

import pytest

import config

@pytest.fixture
def testconfig():
    """Change configuration values for easier test writing"""
    config.STRING_LENTH = 10
    config.NUMBER_OF_ROWS = 5
    config.MAX_NUMBER_OF_DATA = 20
    return "Test configuration applied"
