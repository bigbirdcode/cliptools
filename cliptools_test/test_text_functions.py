"""ClipTools clipboard manager and text processing tools
with a lines based GUI interface

Test

Text processing functions used to change active text content
"""


import unittest  # pylint: disable=unused-import
import doctest

from cliptools_test import config_test  # pylint: disable=unused-import
# pragma pylint: disable=missing-docstring

from cliptools_app import text_functions
from cliptools_app import sanitize


def load_tests(loader, tests, ignore):  # pylint: disable=unused-argument
    # Main goal is to execute the doctests as unittest
    # for all defined text functions
    tests.addTests(doctest.DocTestSuite(text_functions))
    # But then execute the doctests by Luciano Ramalho
    tests.addTests(doctest.DocTestSuite(sanitize))
    return tests
