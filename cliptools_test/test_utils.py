"""ClipTools clipboard manager and text processing tools
with a lines based GUI interface

Test

Utility functions
"""

import unittest

from cliptools_test import config_test  # pylint: disable=unused-import
# pragma pylint: disable=missing-docstring

from cliptools_app import utils

def action_good(text):
    return "good:" + text

def action_wrong(text):
    return str(1/0) + text

class TestUtils(unittest.TestCase):

    def test_limit_text_short(self):
        in_txt = "Short\ntext"
        ou_txt = "Short text"
        self.assertEqual(utils.limit_text(in_txt), ou_txt)

    def test_limit_text_long(self):
        in_txt = "Long\nand\nboring\ntext"
        ou_txt = "Long [...]"
        self.assertEqual(utils.limit_text(in_txt), ou_txt)

    def test_safe_action_good(self):
        self.assertEqual(utils.safe_action("good", action_good), "good:good")

    def test_safe_action_wrong(self):
        self.assertEqual(utils.safe_action("wrong", action_wrong), "ERROR: division by zero")
