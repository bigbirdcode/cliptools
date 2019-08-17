"""ClipTools clipboard manager and text processing tools
with a lines based GUI interface

Test

Definition of data structures used to store text and action data
"""

import unittest

from cliptools_test import config_test  # pylint: disable=unused-import
# pragma pylint: disable=missing-docstring

from cliptools_app import data_struct

def text_range(number):
    return [str(i) for i in range(number)]


class TestBaseData(unittest.TestCase):

    """
    Test the class BaseData
    """

    def test_base_init_empty(self):
        sut = data_struct.BaseData('SUT')
        with self.assertRaises(IndexError):
            sut.get_content(0)
        sut = data_struct.BaseData('SUT', None)
        with self.assertRaises(IndexError):
            sut.get_content(0)

    def test_base_init_get_content(self):
        sut = data_struct.BaseData('SUT', ['0', '1'])
        self.assertEqual(sut.get_content(0), '0')
        self.assertEqual(sut.get_content(1), '1')

    def test_base_init_get_content_out(self):
        sut = data_struct.BaseData('SUT', text_range(10))
        self.assertEqual(sut.get_content(4), '4')
        with self.assertRaises(IndexError):
            sut.get_content(5)

    def test_base_init_get_name(self):
        sut = data_struct.BaseData('SUT', ['0', 'Long\nand\nboring\ntext'])
        self.assertEqual(sut.get_name(0), '0')
        self.assertEqual(sut.get_name(1), 'Long [...]')
        self.assertEqual(sut.get_name(0, 'optional text'), '0')

    def test_base_add_content_end(self):
        sut = data_struct.BaseData('SUT', ['0', '1'])
        sut.add_content('2')
        sut.add_content('3', True)
        sut.add_content('4', end=True)
        sut.add_content('5')  # test addition after NUMBER_OF_ROWS
        self.assertEqual(sut.get_content(1), '1')
        self.assertEqual(sut.get_content(2), '2')
        self.assertEqual(sut.get_content(3), '3')
        self.assertEqual(sut.get_content(4), '4')

    def test_base_add_content_begin(self):
        sut = data_struct.BaseData('SUT', ['0', '1'])
        sut.add_content('-1', None)
        sut.add_content('-2', end=False)
        self.assertEqual(sut.get_content(0), '-2')
        self.assertEqual(sut.get_content(1), '-1')
        self.assertEqual(sut.get_content(2), '0')

    def test_base_add_content_empty(self):
        sut = data_struct.BaseData('SUT', [])
        sut.add_content('-1', end=False)
        self.assertEqual(sut.get_content(0), '-1')
        sut = data_struct.BaseData('SUT', [])
        sut.add_content('1', end=True)
        self.assertEqual(sut.get_content(0), '1')

    def test_base_add_content_full_end(self):
        sut = data_struct.BaseData('SUT', text_range(19))
        self.assertEqual(len(sut.contents), 19)
        sut.add_content('19', end=True)
        self.assertEqual(len(sut.contents), 20)
        sut.add_content('20', end=True)
        self.assertEqual(len(sut.contents), 20)
        self.assertEqual(sut.get_content(0), '1')

    def test_base_add_content_full_begin(self):
        sut = data_struct.BaseData('SUT', text_range(19))
        self.assertEqual(len(sut.contents), 19)
        sut.add_content('-1', end=False)
        self.assertEqual(len(sut.contents), 20)
        sut.add_content('-2', end=False)
        self.assertEqual(len(sut.contents), 20)
        self.assertEqual(sut.get_content(0), '-2')

    def test_base_long_list(self):
        sut = data_struct.BaseData('SUT', text_range(6))
        self.assertEqual(sut.get_content(0), '0')
        self.assertEqual(sut.get_content(1), '1')
        self.assertEqual(sut.get_content(4), '4')

    def test_base_page_down_1(self):
        sut = data_struct.BaseData('SUT', text_range(6))
        sut.page_down()
        self.assertEqual(sut.get_content(0), '5')
        with self.assertRaises(IndexError):
            sut.get_content(1)

    def test_base_page_down_2(self):
        sut = data_struct.BaseData('SUT', text_range(15))
        sut.page_down()
        sut.page_down()
        self.assertEqual(sut.get_content(0), '10')
        self.assertEqual(sut.get_content(4), '14')

    def test_base_page_down_out(self):
        sut = data_struct.BaseData('SUT', text_range(15))
        sut.page_down()
        sut.page_down()
        sut.page_down()
        self.assertEqual(sut.get_content(0), '10')
        self.assertEqual(sut.get_content(4), '14')

    def test_base_page_up(self):
        sut = data_struct.BaseData('SUT', text_range(15))
        sut.page_down()
        sut.page_down()
        sut.page_up()
        self.assertEqual(sut.get_content(0), '5')
        self.assertEqual(sut.get_content(4), '9')

    def test_base_page_up_out(self):
        sut = data_struct.BaseData('SUT', text_range(15))
        sut.page_down()
        sut.page_up()
        sut.page_up()
        self.assertEqual(sut.get_content(0), '0')
        self.assertEqual(sut.get_content(4), '4')

    def test_base_page_down_with_add(self):
        # note: keeping current position
        sut = data_struct.BaseData('SUT', text_range(15))
        sut.page_down()
        sut.add_content('-1', end=False)
        self.assertEqual(sut.get_content(0), '5')
        self.assertEqual(sut.get_content(4), '9')

    def test_base_page_up_with_add(self):
        sut = data_struct.BaseData('SUT', text_range(15))
        sut.page_down()
        sut.add_content('-1', end=False)
        sut.page_up()
        self.assertEqual(sut.get_content(0), '0')
        sut.page_up()
        self.assertEqual(sut.get_content(0), '-1')
        self.assertEqual(sut.get_content(1), '0')

    def test_base_get_names(self):
        sut = data_struct.BaseData('SUT', ['0', '1'])
        self.assertEqual(list(sut.get_names()), ['0', '1', '', '', ''])
        self.assertEqual(list(sut.get_names('optional text')), ['0', '1', '', '', ''])

    def test_base_get_names_long(self):
        sut = data_struct.BaseData('SUT', text_range(6))
        self.assertEqual(list(sut.get_names()), ['0', '1', '2', '3', '4'])


class TestTextData(unittest.TestCase):

    """
    Test the class TextData
    """

    def test_text_add_content(self):
        sut = data_struct.TextData('SUT', ['0', '1'])
        sut.add_content('-1')
        self.assertEqual(sut.get_content(0), '-1')
        self.assertEqual(sut.get_content(1), '0')


class TestActionData(unittest.TestCase):

    """
    Test the class ActionData
    """

    def test_action_add_and_get_content(self):
        sut = data_struct.ActionData('SUT')
        sut.add_content(('0', str.lower))
        self.assertEqual(sut.get_content(0), str.lower)

    def test_action_add_duplicate_content(self):
        sut = data_struct.ActionData('SUT')
        sut.add_content(('0', str.lower))
        with self.assertRaises(RuntimeError):
            sut.add_content(('0', str.lower))

    def test_action_get_name(self):
        sut = data_struct.ActionData('SUT')
        sut.add_content(('0', str.lower))
        self.assertEqual(sut.get_name(0, 'FOo'), '0: foo')

    def test_action_get_name_wrong(self):
        sut = data_struct.ActionData('SUT')
        sut.add_content(('0', lambda x: str(1 / float(x))))
        self.assertEqual(sut.get_name(0, '0'), '0: ERROR[...]')


class TestDataCollection(unittest.TestCase):

    """
    Test the class DataCollection
    """

    def test_collection_get_name(self):
        sut = data_struct.DataCollection('SUT')
        content = data_struct.TextData('zero')
        sut.add_content(content)
        self.assertEqual(sut.get_name(0), 'zero')

    def test_collection_get_content_by_name(self):
        sut = data_struct.DataCollection('SUT')
        content_0 = data_struct.TextData('zero')
        content_1 = data_struct.TextData('one')
        sut.add_content(content_0)
        sut.add_content(content_1)
        self.assertEqual(sut.get_content_by_name('zero'), content_0)
        self.assertEqual(sut.get_content_by_name('one'), content_1)
        with self.assertRaises(RuntimeError):
            sut.get_content_by_name('two')


class TestDataCollections(unittest.TestCase):

    """
    Test the class DataCollections (the "only" one)
    """

    def test_collections_generic(self):
        sut = data_struct.DataCollections()
        self.assertTrue(hasattr(sut, 'texts'))
        self.assertTrue(hasattr(sut, 'actions'))
        sut.texts.get_content_by_name('clips')  # no exception should be raised

    def test_collections_module_attribute(self):
        sut = data_struct.data_collections
        self.assertTrue(hasattr(sut, 'texts'))
        self.assertTrue(hasattr(sut, 'actions'))
        sut.texts.get_content_by_name('clips')  # no exception should be raised

    def test_register_function(self):
        # Note: this test has side effect
        # the registered function may be available during all tests
        # but since unregister is not in the scope it will be there
        def groupname_funcname(txt):
            return txt
        data_struct.register_function(groupname_funcname)
        with self.assertRaises(RuntimeError):
            data_struct.register_function(groupname_funcname)
        actions = data_struct.data_collections.actions.get_content_by_name('groupname')
        self.assertEqual(actions.get_name(0, 'T'), 'funcname: T')
