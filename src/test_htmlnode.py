import unittest
from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_empty(self):
        node = HTMLNode("div")
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_single(self):
        node = HTMLNode("div", props={"class": "my-class"})
        self.assertEqual(node.props_to_html(), ' class="my-class"')

    def test_props_to_html_multiple(self):
        node = HTMLNode("div", props={"class": "my-class", "id": "my-id"})
        self.assertEqual(node.props_to_html(), ' class="my-class" id="my-id"')
        


if __name__ == "__main__":
    unittest.main()