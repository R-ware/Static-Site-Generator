import unittest
from source_copy import extract_title

class TestSourceCopy(unittest.TestCase):
    def test_extract_title_with_h1(self):
        md = "# Hello World!"
        output = extract_title(md)
        expected_result = "Hello World!"
        self.assertEqual(output, expected_result)

    def test_extract_title_without_h1(self):
        md = "There is no h1 header"
        with self.assertRaises(Exception):
            extract_title(md)

    def test_extract_title_extra_whitespace(self):
        md = "  #   There is   extra spacing.   "
        output = extract_title(md)
        expected_result = "There is extra spacing."
        self.assertEqual(output, expected_result)

    