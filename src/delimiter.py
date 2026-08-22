from textnode import TextNode, TextType, text_node_to_html_node
import re
from enum import Enum
from htmlnode import *

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.text_inline:
            new_nodes.append(node)
            continue
        parts = node.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise ValueError(f"Delimiter '{delimiter}' is not closed in text: {node.text}")
        for i, part in enumerate(parts):
            if part == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(part, TextType.text_inline))
            else:
                new_nodes.append(TextNode(part, text_type))
    return new_nodes

def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    image_matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return image_matches

def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    link_matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return link_matches

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.text_inline:
            new_nodes.append(node)
            continue
        image_matches = extract_markdown_images(node.text)
        if not image_matches:
            new_nodes.append(node)
            continue
        last_index = 0
        for match in image_matches:
            alt_text, url = match
            start_index = node.text.find(f"![{alt_text}]({url})", last_index)
            if start_index > last_index:
                new_nodes.append(TextNode(node.text[last_index:start_index], TextType.text_inline))
            new_nodes.append(TextNode(f"{alt_text}", TextType.images_inline, url=url))
            last_index = start_index + len(f"![{alt_text}]({url})")
        if last_index < len(node.text):
            new_nodes.append(TextNode(node.text[last_index:], TextType.text_inline))
    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.text_inline:
            new_nodes.append(node)
            continue
        link_matches = extract_markdown_links(node.text)
        if not link_matches:
            new_nodes.append(node)
            continue
        last_index = 0
        for match in link_matches:
            link_text, url = match
            start_index = node.text.find(f"[{link_text}]({url})", last_index)
            if start_index > last_index:
                new_nodes.append(TextNode(node.text[last_index:start_index], TextType.text_inline))
            new_nodes.append(TextNode(f"{link_text}", TextType.links_inline, url=url))
            last_index = start_index + len(f"[{link_text}]({url})")
        if last_index < len(node.text):
            new_nodes.append(TextNode(node.text[last_index:], TextType.text_inline))
    return new_nodes

def text_to_textnodes(text: str) -> list[TextNode]:
    nodes = [TextNode(text, TextType.text_inline)]
    nodes = split_nodes_delimiter(nodes, "*", TextType.bold_inline)
    nodes = split_nodes_delimiter(nodes, "_", TextType.italic_inline)
    nodes = split_nodes_delimiter(nodes, "`", TextType.code_inline)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def markdown_to_blocks(text: str) -> list[str]:
    lines = text.split("\n\n")
    blocks = []
    for line in lines:
        stripped_line = line.strip()
        if stripped_line == "":
            continue
        elif stripped_line:
            blocks.append(stripped_line)
    return blocks

class BlockType(Enum):
    paragraph = "paragraph"
    heading = "heading"
    quote = "quote"
    code = "code"
    unordered_list = "unordered_list"
    ordered_list = "ordered_list"

def block_to_block_type(block: str) -> BlockType:
    lines = block.split("\n")
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.heading
    elif block.startswith("```") and block.endswith("```"):
        return BlockType.code
    elif all(line.startswith((">", "> ")) for line in lines):
        return BlockType.quote
    elif all(line.startswith("- ") for line in lines):
        return BlockType.unordered_list
    elif block.startswith("1. "):
        if all(line.startswith(f"{i}. ") for i, line in enumerate(lines, start=1)):
            return BlockType.ordered_list
        else:
            return BlockType.paragraph
    else:
        return BlockType.paragraph

def text_to_children(text: str) -> list[HTMLNode]:
    text_nodes = text_to_textnodes(text)
    html_nodes = [text_node_to_html_node(node) for node in text_nodes]
    return html_nodes

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.paragraph:
            lines = block.split("\n")
            stripped_lines = [line.strip() for line in lines]
            paragraph_text = " ".join(stripped_lines)
            children = text_to_children(paragraph_text)
            html_nodes.append(ParentNode("p", children))
        if block_type == BlockType.heading:
            header_parts = block.split(" ", 1)
            header_level = f"h{len(header_parts[0])}"
            children = text_to_children(header_parts[1])
            html_nodes.append(ParentNode(header_level, children))
        if block_type == BlockType.quote:
            quote_lines = block.split("\n")
            stripped_quote_lines = [quote_line[1:].strip() for quote_line in quote_lines]
            quote_text = " ".join(stripped_quote_lines)
            children = text_to_children(quote_text)
            html_nodes.append(ParentNode("blockquote", children))                


    return ParentNode("div", html_nodes)