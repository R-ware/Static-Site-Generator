import unittest
from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.bold_inline)
        node2 = TextNode("This is a text node", TextType.bold_inline)
        self.assertEqual(node, node2)

    def test_url_none(self):
        node = TextNode("This is a text node", TextType.bold_inline)
        node2 = TextNode("This is a text node", TextType.bold_inline, url=None)
        self.assertEqual(node, node2)

    def test_texttype(self):
        node = TextNode("This is a text node", TextType.bold_inline)
        node2 = TextNode("This is a text node", TextType.text_inline)
        self.assertNotEqual(node, node2)

    def test_texttype_url(self):
        node = TextNode("This is a text node", TextType.bold_inline)
        node2 = TextNode("This is a text node", TextType.text_inline, url="http://example.com")
        self.assertNotEqual(node, node2)
        


if __name__ == "__main__":
    unittest.main()