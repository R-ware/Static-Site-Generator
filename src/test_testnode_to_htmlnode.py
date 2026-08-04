import unittest
from enum import Enum
from htmlnode import ParentNode, LeafNode
from textnode import TextNode, TextType, text_node_to_html_node

class TestTextNodeToHtmlNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.text_inline)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is bold text", TextType.bold_inline)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold text")

    def test_italic(self):
        node = TextNode("This is italic text", TextType.italic_inline)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is italic text")

    def test_code(self):
        node = TextNode("This is code text", TextType.code_inline)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is code text")

    def test_link(self):    
        node = TextNode("This is a link", TextType.links_inline, url="https://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link")
        self.assertEqual(html_node.props, {"href": "https://example.com"})

    def test_image(self):
        node = TextNode("This is an image", TextType.images_inline, url="https://example.com/image.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertIsNone(html_node.value)
        self.assertEqual(html_node.props, {"src": "https://example.com/image.png", "alt": "This is an image"})

    def test_link_without_url(self):
        node = TextNode("This is a link", TextType.links_inline)
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)

    def test_image_without_url(self):
        node = TextNode("This is an image", TextType.images_inline)
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)

    def test_unsupported_text_type(self):
        class UnsupportedTextType(Enum):
            unsupported = "unsupported"
        node = TextNode("This is unsupported", UnsupportedTextType.unsupported)
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.text_inline)
        self.assertEqual(repr(node), "TextNode(This is a text node, text, None)")