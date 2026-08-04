from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    text_inline = "text"
    bold_inline = "bold"
    italic_inline = "italic"
    code_inline = "code"
    links_inline = "links"
    images_inline = "images"

class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if not isinstance(other, TextNode):
            return False
        return (self.text == other.text and
                self.text_type == other.text_type and
                self.url == other.url)
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

def text_node_to_html_node(text_node: TextNode) -> 'LeafNode':
    if text_node.text_type == TextType.text_inline:
        return LeafNode(None, text_node.text)
    elif text_node.text_type == TextType.bold_inline:
        return LeafNode("b", text_node.text)
    elif text_node.text_type == TextType.italic_inline:
        return LeafNode("i", text_node.text)
    elif text_node.text_type == TextType.code_inline:
        return LeafNode("code", text_node.text)
    elif text_node.text_type == TextType.links_inline:
        if text_node.url is None:
            raise ValueError("URL was not provided for a link text node.")
        return LeafNode("a", text_node.text, props={"href": text_node.url})
    elif text_node.text_type == TextType.images_inline:
        if text_node.url is None:
            raise ValueError("URL was not provided for an image text node.")
        return LeafNode("img", None, props={"src": text_node.url, "alt": text_node.text})
    else:
        raise ValueError(f"Unsupported text type: {text_node.text_type}")
    