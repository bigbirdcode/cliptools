"""
ClipTools clipboard manager and text processing tools
with a lines based GUI interface

Test

Definition of data structures used to store text and action data
"""

# ruff: noqa: D103 - missing docstring

import pytest

from cliptools.modules import data_struct


def text_range(number):
    return [str(i) for i in range(number)]


###########################################################
# Test the class BaseData
###########################################################


def test_base_init_empty():
    sut = data_struct.BaseData("SUT")
    with pytest.raises(IndexError):
        sut.get_content(0)


def test_base_init_get_content():
    sut = data_struct.BaseData("SUT", ["0", "1"])
    assert sut.get_content(0) == "0"
    assert sut.get_content(1) == "1"


def test_base_init_get_content_out_of_rows(test_config):
    sut = data_struct.BaseData("SUT", text_range(10))
    sut.set_config(test_config)
    assert sut.get_content(4) == "4"
    with pytest.raises(IndexError):
        sut.get_content(5)


def test_base_init_get_name(test_config):
    sut = data_struct.BaseData("SUT", ["0", "Long\nand\nboring\ntext"])
    sut.set_config(test_config)
    assert sut.get_name(0) == "0"
    assert sut.get_name(1) == "Long [...]"
    assert sut.get_name(0, "optional text") == "0"


def test_base_add_content_end(test_config):
    sut = data_struct.BaseData("SUT", ["0", "1"])
    sut.set_config(test_config)
    sut.add_content("2")
    sut.add_content("3", True)
    sut.add_content("4", end=True)
    sut.add_content("5")  # test addition after NUMBER_OF_ROWS
    assert sut.get_content(1) == "1"
    assert sut.get_content(2) == "2"
    assert sut.get_content(3) == "3"
    assert sut.get_content(4) == "4"
    with pytest.raises(IndexError):
        sut.get_content(5)


def test_base_add_content_begin(test_config):
    sut = data_struct.BaseData("SUT", ["0", "1"])
    sut.set_config(test_config)
    sut.add_content("-1", None)
    sut.add_content("-2", end=False)
    assert sut.get_content(0) == "-2"
    assert sut.get_content(1) == "-1"
    assert sut.get_content(2) == "0"


def test_base_add_content_empty():
    sut = data_struct.BaseData("SUT", [])
    sut.add_content("-1", end=False)
    assert sut.get_content(0) == "-1"
    sut = data_struct.BaseData("SUT", [])
    sut.add_content("1", end=True)
    assert sut.get_content(0) == "1"


def test_base_add_content_full_end(test_config):
    sut = data_struct.BaseData("SUT", text_range(19))
    sut.set_config(test_config, need_max=True)
    assert len(sut.contents) == 19
    sut.add_content("19", end=True)
    assert len(sut.contents) == 20
    sut.add_content("20", end=True)
    assert len(sut.contents) == 20
    assert sut.get_content(0) == "1"


def test_base_add_content_full_begin(test_config):
    sut = data_struct.BaseData("SUT", text_range(19))
    sut.set_config(test_config, need_max=True)
    assert len(sut.contents) == 19
    sut.add_content("-1", end=False)
    assert len(sut.contents) == 20
    sut.add_content("-2", end=False)
    assert len(sut.contents) == 20
    assert sut.get_content(0) == "-2"


def test_base_long_list(test_config):
    sut = data_struct.BaseData("SUT", text_range(6))
    sut.set_config(test_config)
    assert sut.get_content(0) == "0"
    assert sut.get_content(1) == "1"
    assert sut.get_content(4) == "4"


def test_base_page_down_1(test_config):
    sut = data_struct.BaseData("SUT", text_range(6))
    sut.set_config(test_config)
    sut.page_down()
    assert sut.get_content(0) == "5"
    with pytest.raises(IndexError):
        sut.get_content(1)


def test_base_page_down_2(test_config):
    sut = data_struct.BaseData("SUT", text_range(15))
    sut.set_config(test_config)
    sut.page_down()
    sut.page_down()
    assert sut.get_content(0) == "10"
    assert sut.get_content(4) == "14"


def test_base_page_down_out(test_config):
    sut = data_struct.BaseData("SUT", text_range(15))
    sut.set_config(test_config)
    sut.page_down()
    sut.page_down()
    sut.page_down()
    assert sut.get_content(0) == "10"
    assert sut.get_content(4) == "14"


def test_base_page_up(test_config):
    sut = data_struct.BaseData("SUT", text_range(15))
    sut.set_config(test_config)
    sut.page_down()
    sut.page_down()
    sut.page_up()
    assert sut.get_content(0) == "5"
    assert sut.get_content(4) == "9"


def test_base_page_up_out(test_config):
    sut = data_struct.BaseData("SUT", text_range(15))
    sut.set_config(test_config)
    sut.page_down()
    sut.page_up()
    sut.page_up()
    assert sut.get_content(0) == "0"
    assert sut.get_content(4) == "4"


def test_base_page_down_with_add(test_config):
    # note: keeping current position
    sut = data_struct.BaseData("SUT", text_range(15))
    sut.set_config(test_config)
    sut.page_down()
    sut.add_content("-1", end=False)
    assert sut.get_content(0) == "5"
    assert sut.get_content(4) == "9"


def test_base_page_up_with_add(test_config):
    sut = data_struct.BaseData("SUT", text_range(15))
    sut.set_config(test_config)
    sut.page_down()
    sut.add_content("-1", end=False)
    sut.page_up()
    assert sut.get_content(0) == "0"
    sut.page_up()
    assert sut.get_content(0) == "-1"
    assert sut.get_content(1) == "0"


def test_base_get_names(test_config):
    sut = data_struct.BaseData("SUT", ["0", "1"])
    sut.set_config(test_config)
    assert list(sut.get_names()) == ["0", "1", "", "", ""]
    assert list(sut.get_names("optional text")) == ["0", "1", "", "", ""]


def test_base_get_names_long(test_config):
    sut = data_struct.BaseData("SUT", text_range(6))
    sut.set_config(test_config)
    assert list(sut.get_names()) == ["0", "1", "2", "3", "4"]


def test_base_get_focus(test_config):
    sut = data_struct.BaseData("SUT", text_range(6))
    sut.set_config(test_config)
    assert sut.get_focused_content() == "0"


def test_base_set_and_get_focus(test_config):
    sut = data_struct.BaseData("SUT", text_range(6))
    sut.set_config(test_config)
    sut.set_focus(2)
    assert sut.get_focused_content() == "2"
    sut.set_focus(5)  # out of view, no change
    assert sut.get_focused_content() == "2"


def test_base_focus_up(test_config):
    sut = data_struct.BaseData("SUT", text_range(6))
    sut.set_config(test_config)
    sut.set_focus(2)
    sut.focus_up()
    assert sut.get_focused_content() == "1"


def test_base_focus_down(test_config):
    sut = data_struct.BaseData("SUT", text_range(6))
    sut.set_config(test_config)
    sut.set_focus(2)
    sut.focus_down()
    assert sut.get_focused_content() == "3"


def test_base_focus_page_down_short(test_config):
    sut = data_struct.BaseData("SUT", text_range(6))
    sut.set_config(test_config)
    sut.set_focus(2)
    sut.page_down()
    assert sut.get_focused_content() == "5"


def test_base_focus_page_down_long(test_config):
    sut = data_struct.BaseData("SUT", text_range(10))
    sut.set_config(test_config)
    sut.set_focus(2)
    sut.page_down()
    assert sut.get_focused_content() == "7"
    sut.page_down()
    assert sut.get_focused_content() == "9"


def test_base_focus_page_up_simple(test_config):
    sut = data_struct.BaseData("SUT", text_range(10))
    sut.set_config(test_config)
    sut.set_focus(2)
    sut.page_down()
    sut.page_up()
    assert sut.get_focused_content() == "2"


def test_base_focus_page_up_short(test_config):
    sut = data_struct.BaseData("SUT", text_range(6))
    sut.set_config(test_config)
    sut.set_focus(2)
    sut.page_up()
    assert sut.get_focused_content() == "0"


def test_base_focus_with_add_end(test_config):
    sut = data_struct.BaseData("SUT", ["0", "1"])
    sut.set_config(test_config)
    sut.add_content("2")
    assert sut.get_focused_content() == "0"
    sut.set_focus(2)
    sut.add_content("3")
    assert sut.get_focused_content() == "2"


def test_base_focus_with_add_begin(test_config):
    sut = data_struct.BaseData("SUT", ["0", "1"])
    sut.set_config(test_config)
    assert sut.get_focused_content() == "0"
    sut.add_content("-1", end=False)  # focus stay at index 0
    assert sut.get_focused_content() == "-1"
    sut.set_focus(2)  # focus is at index 2, that is '1'
    sut.add_content("-2", end=False)  # focus moves with item
    assert sut.get_focused_content() == "1"


def test_base_focus_with_add_begin_full(test_config):
    sut = data_struct.BaseData("SUT", text_range(6))
    sut.set_config(test_config)
    sut.set_focus(4)  # focus is at last possible index
    sut.add_content("-1", end=False)
    assert sut.get_focused_content() == "3"


def test_base_focus_with_add_begin_page_down(test_config):
    sut = data_struct.BaseData("SUT", text_range(6))
    sut.set_config(test_config)
    sut.page_down()
    sut.add_content("-1", end=False)  # no change
    assert sut.get_focused_content() == "5"


def test_base_focus_with_add_begin_page_down_full(test_config):
    sut = data_struct.BaseData("SUT", text_range(10))
    sut.set_config(test_config)
    sut.set_focus(4)  # focus is at last possible index
    sut.page_down()
    sut.add_content("-1", end=False)  # no change
    assert sut.get_focused_content() == "9"


def test_is_first_selected_1(test_config):
    sut = data_struct.BaseData("SUT", text_range(10))
    sut.set_config(test_config)
    assert sut.is_first_selected()


def test_is_first_selected_2(test_config):
    sut = data_struct.BaseData("SUT", text_range(10))
    sut.set_config(test_config)
    sut.set_focus(4)
    assert not sut.is_first_selected()


def test_is_first_selected_3():
    sut = data_struct.BaseData("SUT", text_range(10))
    sut.page_down()
    assert not sut.is_first_selected()


###########################################################
# Test the class TextData
###########################################################


def test_text_add_content():
    sut = data_struct.TextData("SUT", ["0", "1"])
    sut.add_content("-1")
    assert sut.get_content(0) == "-1"
    assert sut.get_content(1) == "0"


###########################################################
# Test the class ActionData
###########################################################


def test_action_add_and_get_content():
    sut = data_struct.ActionData("SUT")
    sut.add_content(("0", str.lower))
    assert sut.get_content(0) == str.lower


def test_action_add_duplicate_content():
    sut = data_struct.ActionData("SUT")
    sut.add_content(("0", str.lower))
    with pytest.raises(RuntimeError):
        sut.add_content(("0", str.lower))


def test_action_get_name():
    sut = data_struct.ActionData("SUT")
    sut.add_content(("0", str.lower))
    assert sut.get_name(0, "FOo") == "0: foo"


def test_action_get_name_wrong(test_config):
    sut = data_struct.ActionData("SUT")
    sut.set_config(test_config)
    sut.add_content(("0", lambda x: str(1 / float(x))))
    assert sut.get_name(0, "0") == "0: ERROR[...]"


def test_action_get_names(test_config):
    sut = data_struct.ActionData("SUT")
    sut.set_config(test_config)
    sut.add_content(("0", str.lower))
    sut.add_content(("1", str.upper))
    assert list(sut.get_names("FOo")) == ["0: foo", "1: FOO", "", "", ""]


###########################################################
# Test the class DataCollection
###########################################################


def test_collection_get_name():
    sut = data_struct.DataCollection("SUT")
    content = data_struct.TextData("zero")
    sut.add_content(content)
    assert sut.get_name(0) == "zero"


def test_collection_get_content_by_name():
    sut = data_struct.DataCollection("SUT")
    content_0 = data_struct.TextData("zero")
    content_1 = data_struct.TextData("one")
    sut.add_content(content_0)
    sut.add_content(content_1)
    assert sut.get_content_by_name("zero") == content_0
    assert sut.get_content_by_name("one") == content_1
    with pytest.raises(RuntimeError):
        sut.get_content_by_name("two")


###########################################################
# Test the class DataCollections (the "only" one)
###########################################################


def test_collections_generic():
    sut = data_struct.DataCollections()
    assert hasattr(sut, "texts")
    assert hasattr(sut, "actions")
    sut.texts.get_content_by_name("clips")  # no exception should be raised


def test_register_function():
    # Note: this test has side effect
    # the registered function may be available during all tests
    # but since unregister is not in the scope it will be there
    def groupname_funcname(txt):
        return txt

    data_struct.register_function(groupname_funcname)
    with pytest.raises(RuntimeError):
        data_struct.register_function(groupname_funcname)
    actions = data_struct.DataCollections().actions.get_content_by_name("groupname")
    assert actions.get_name(0, "T") == "funcname: T"
