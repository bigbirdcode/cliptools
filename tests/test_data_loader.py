"""
ClipTools clipboard manager and text processing tools
with a lines based GUI interface

Test

Data loader functions
"""

# ruff: noqa: D103 - missing docstring

import shutil

from cliptools.modules import data_struct


def test_load_yml_data(test_resources, tmp_path):
    shutil.copy(test_resources / "text_data.yml", tmp_path)
    sut = data_struct.DataCollections()
    sut.load_data(tmp_path)
    assert "yaml_data" in sut.texts.get_names()
    assert sut.texts.get_content(0).name == "clips"
    text_data = sut.texts.get_content(1)
    assert text_data.name == "yaml_data"
    assert text_data.contents == ["A", "B", "C"]
