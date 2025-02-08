"""
ClipTools clipboard manager and text processing tools
with a lines based GUI interface

Test

Config file reading test
"""

# ruff: noqa: D103 - missing docstring

import pathlib
import shutil

from cliptools.modules import config, data_struct


def test_sample_config(src_samples):
    sample_config = src_samples / "config.yml"
    c = config.read_config(pathlib.Path(), config_file=sample_config)
    assert not isinstance(c, str), c
    assert c.port == 5555


def test_load_yml_data(src_samples, test_config, tmp_path):
    shutil.copy(src_samples / "text_data.yml", tmp_path)
    sut = data_struct.DataCollections()
    sut.set_config(test_config)
    sut.load_data(tmp_path)
    assert list(sut.texts.get_names()) == [
        "clips",
        "yaml_samples",
        "sniplets",
        "my_data",
        "some data",
    ]
    text_data = sut.texts.get_content(1)
    assert text_data.name == "yaml_samples"
    assert text_data.contents[1] == "árvíztűrő tükörfúrógép"
