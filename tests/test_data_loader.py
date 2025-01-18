"""ClipTools clipboard manager and text processing tools
with a lines based GUI interface

Test

Data loader functions
"""

# pragma pylint: disable=missing-docstring,unused-argument

import pathlib

import pytest

from cliptools import config
from cliptools.modules import data_loader


PYTHON_TEXT_DATA = pathlib.Path("tests/test_resources/text_data.py")
YAML_TEXT_DATA = pathlib.Path("tests/test_resources/text_data.yml")
UNKNOWN_TEXT_DATA = pathlib.Path("tests/test_resources/text_data.txt")
PYTHON_WRONG_DATA = pathlib.Path("tests/test_resources/wrong_data.py")
YAML_WRONG_DATA = pathlib.Path("tests/test_resources/wrong_data.yml")

# Note on testing:
# files in tests/test_resources are used
# user personal folder is not tested, to avoid messing up user data

#######################
# Testing lowest level


def test_load_yml_data():
    result = data_loader.load_ext_yml_data(YAML_TEXT_DATA)
    assert result["yaml_data"] == ["A", "B", "C"]


def test_load_py_data():
    result = data_loader.load_ext_py_data(PYTHON_TEXT_DATA)
    assert result["python_data"] == ["D", "E", "F"]


def test_load_sample_data():
    result = data_loader.load_sample_data()
    assert result["some data"] == ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10"]


#######################
# Testing middle level


def test_load_ext_data_yml():
    result = data_loader.load_ext_data(YAML_TEXT_DATA)
    assert result["yaml_data"] == ["A", "B", "C"]


def test_load_ext_data_py():
    result = data_loader.load_ext_data(PYTHON_TEXT_DATA)
    assert result["python_data"] == ["D", "E", "F"]


def test_load_ext_data_unknownk():
    with pytest.raises(RuntimeError):
        data_loader.load_ext_data(UNKNOWN_TEXT_DATA)


#######################
# Testing highest level


def test_load_data_py():
    # Load python from absolute path
    config.EXTERNAL_DATA = PYTHON_TEXT_DATA.resolve()
    result = data_loader.load_data()
    assert result["python_data"] == ["D", "E", "F"]


def test_load_data_yml():
    # Load yaml from absolute path
    config.EXTERNAL_DATA = YAML_TEXT_DATA.resolve()
    result = data_loader.load_data()
    assert result["yaml_data"] == ["A", "B", "C"]


def test_load_data_nonexistent():
    # Default is loaded
    config.EXTERNAL_DATA = UNKNOWN_TEXT_DATA
    result = data_loader.load_data()
    assert result["some data"] == ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10"]


def test_load_data_wrong_py():
    # Default is loaded
    config.EXTERNAL_DATA = PYTHON_WRONG_DATA.resolve()
    result = data_loader.load_data()
    assert result["some data"] == ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10"]


def test_load_data_wrong_yml():
    # Default is loaded
    config.EXTERNAL_DATA = YAML_WRONG_DATA.resolve()
    result = data_loader.load_data()
    assert result["some data"] == ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10"]
