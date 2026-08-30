import unittest
from textnode import TextNode, TextType
from delimiter import markdown_to_html_node, split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_children, text_to_textnodes, markdown_to_blocks, BlockType, block_to_block_type
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_nodes_delimiter_bold1(self):
        node = TextNode("This is some text with **bold** and _italic_ formatting", TextType.text_inline)
        new_nodes = split_nodes_delimiter([node], "**", TextType.bold_inline)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is some text with ", TextType.text_inline),
                TextNode("bold", TextType.bold_inline),
                TextNode(" and _italic_ formatting", TextType.text_inline),
            ],
        )

    def test_split_nodes_delimiter_bold2(self):
        node = TextNode("This is some text with **bold** and _italic_ formatting", TextType.text_inline)
        new_nodes = split_nodes_delimiter([node], "**", TextType.bold_inline)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is some text with ", TextType.text_inline),
                TextNode("bold", TextType.bold_inline),
                TextNode(" and _italic_ formatting", TextType.text_inline),
            ],
        )
        
    def test_split_nodes_delimiter_italic(self):
        node = TextNode("This is some text with *bold* and _italic_ formatting", TextType.text_inline)
        new_nodes = split_nodes_delimiter([node], "_", TextType.italic_inline)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is some text with *bold* and ", TextType.text_inline),
                TextNode("italic", TextType.italic_inline),
                TextNode(" formatting", TextType.text_inline),
            ],
        )
        
    def test_split_nodes_delimiter_no_delimiters(self):
        node = TextNode("This is some text with no delimiters", TextType.text_inline)
        new_nodes = split_nodes_delimiter([node], "*", TextType.bold_inline)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is some text with no delimiters", TextType.text_inline),
            ],
        )

    def test_split_nodes_delimiter_unmatched_delimiter(self):
        node = TextNode("This is some text with an unmatched * delimiter", TextType.text_inline)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "*", TextType.bold_inline)

    def test_split_nodes_delimiter_non_text_node(self):
        node = TextNode("This is some text with *bold* and _italic_ formatting", TextType.bold_inline)
        new_nodes = split_nodes_delimiter([node], "*", TextType.bold_inline)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is some text with *bold* and _italic_ formatting", TextType.bold_inline),
            ],
        )
        
    def test_split_nodes_delimiter_empty_string(self):
        node = TextNode("", TextType.text_inline)
        new_nodes = split_nodes_delimiter([node], "*", TextType.bold_inline)
        self.assertListEqual(new_nodes, [])

    def test_split_nodes_delimiter_multiple_delimiters(self):
        node = TextNode("This is *bold* and *another bold* text", TextType.text_inline)
        new_nodes = split_nodes_delimiter([node], "*", TextType.bold_inline)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is ", TextType.text_inline),
                TextNode("bold", TextType.bold_inline),
                TextNode(" and ", TextType.text_inline),
                TextNode("another bold", TextType.bold_inline),
                TextNode(" text", TextType.text_inline),
            ],
        )

    def test_delimiter_at_start(self):
        node = TextNode("*bold* text", TextType.text_inline)
        new_nodes = split_nodes_delimiter([node], "*", TextType.bold_inline)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("bold", TextType.bold_inline),
                TextNode(" text", TextType.text_inline),
            ],
        )

    def test_delimiter_at_end(self):
        node = TextNode("text *bold*", TextType.text_inline)
        new_nodes = split_nodes_delimiter([node], "*", TextType.bold_inline)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("text ", TextType.text_inline),
                TextNode("bold", TextType.bold_inline),
            ],
        )

    def test_delimiter_with_3_delimiters_unbalanced(self):
        node = TextNode("This is *bold* and *another bold text", TextType.text_inline)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "*", TextType.bold_inline)

    def test_multiple_nodes_with_mixed_types(self):
        nodes = [
            TextNode("This is *bold* text", TextType.text_inline),
            TextNode("This is _italic_ text", TextType.italic_inline),
            TextNode("This is *bold* text", TextType.text_inline),
        ]
        new_nodes = split_nodes_delimiter(nodes, "*", TextType.bold_inline)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is ", TextType.text_inline),
                TextNode("bold", TextType.bold_inline),
                TextNode(" text", TextType.text_inline),
                TextNode("This is _italic_ text", TextType.italic_inline),
                TextNode("This is ", TextType.text_inline),
                TextNode("bold", TextType.bold_inline),
                TextNode(" text", TextType.text_inline),
            ],
        )

    def test_chained_delimiters(self):
        node = TextNode("This is **b_o_ld** and _italic_ text", TextType.text_inline)
        after_bold = split_nodes_delimiter([node], "**", TextType.bold_inline)
        after_italic = split_nodes_delimiter(after_bold, "_", TextType.italic_inline)
        self.assertListEqual(
            after_italic,
            [
                TextNode("This is ", TextType.text_inline),
                TextNode("b_o_ld", TextType.bold_inline),
                TextNode(" and ", TextType.text_inline),
                TextNode("italic", TextType.italic_inline),
                TextNode(" text", TextType.text_inline),
            ],
        )
    def test_empty_node_list(self):
        self.assertListEqual(
            split_nodes_delimiter([], "*", TextType.bold_inline), []
        )

    def test_extract_markdown_images(self):
        image_matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], image_matches)

    def test_extract_markdown_links(self):
        link_matches = extract_markdown_links(
            "This is text with a [link](https://www.example.com)"
        )
        self.assertListEqual([("link", "https://www.example.com")], link_matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.text_inline,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.text_inline),
                TextNode("image", TextType.images_inline, url="https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.text_inline),
                TextNode("second image", TextType.images_inline, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://www.example.com) and another [second link](https://www.example2.com)",
            TextType.text_inline,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.text_inline),
                TextNode("link", TextType.links_inline, url="https://www.example.com"),
                TextNode(" and another ", TextType.text_inline),
                TextNode("second link", TextType.links_inline, url="https://www.example2.com"),
            ],
            new_nodes,
        )

    def test_split_images_no_images(self):
        node = TextNode("This is text with no images", TextType.text_inline)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_split_links_no_links(self):
        node = TextNode("This is text with no links", TextType.text_inline)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    def test_split_images_and_links(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://www.example.com)",
            TextType.text_inline,
        )
        new_nodes_images = split_nodes_image([node])
        new_nodes_links = split_nodes_link(new_nodes_images)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.text_inline),
                TextNode("image", TextType.images_inline, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a ", TextType.text_inline),
                TextNode("link", TextType.links_inline, "https://www.example.com"),
            ],
            new_nodes_links,
        )

    def test_split_images_and_links_no_images(self):
        node = TextNode(
            "This is text with a [link](https://www.example.com) and no images",
            TextType.text_inline,
        )
        new_nodes_images = split_nodes_image([node])
        new_nodes_links = split_nodes_link(new_nodes_images)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.text_inline),
                TextNode("link", TextType.links_inline, "https://www.example.com"),
                TextNode(" and no images", TextType.text_inline),
            ],
            new_nodes_links,
        )

    def test_trailing_text_after_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and some trailing text",
            TextType.text_inline,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.text_inline),
                TextNode("image", TextType.images_inline, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and some trailing text", TextType.text_inline),
            ],
            new_nodes,
        )

    def test_trailing_text_after_link(self):
        node = TextNode(
            "This is text with a [link](https://www.example.com) and some trailing text",
            TextType.text_inline,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.text_inline),
                TextNode("link", TextType.links_inline, "https://www.example.com"),
                TextNode(" and some trailing text", TextType.text_inline),
            ],
            new_nodes,
        )

    def test_leading_text_before_image(self):
        node = TextNode(
            "Leading text before an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.text_inline,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Leading text before an ", TextType.text_inline),
                TextNode("image", TextType.images_inline, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_leading_text_before_link(self):
        node = TextNode(
            "Leading text before a [link](https://www.example.com)",
            TextType.text_inline,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Leading text before a ", TextType.text_inline),
                TextNode("link", TextType.links_inline, "https://www.example.com"),
            ],
            new_nodes,
        )

    def test_image_with_special_characters(self):
        node = TextNode(
            "This is text with an ![image with special characters !@#$%^&*()](https://i.imgur.com/zjjcJKZ.png)",
            TextType.text_inline,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.text_inline),
                TextNode("image with special characters !@#$%^&*()", TextType.images_inline, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        text = "This is **bold**, _italic_, `code`, ![image](https://i.imgur.com/zjjcJKZ.png), and [link](https://www.example.com)."
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            nodes,
            [
                TextNode("This is ", TextType.text_inline),
                TextNode("bold", TextType.bold_inline),
                TextNode(", ", TextType.text_inline),
                TextNode("italic", TextType.italic_inline),
                TextNode(", ", TextType.text_inline),
                TextNode("code", TextType.code_inline),
                TextNode(", ", TextType.text_inline),
                TextNode("image", TextType.images_inline, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(", and ", TextType.text_inline),
                TextNode("link", TextType.links_inline, "https://www.example.com"),
                TextNode(".", TextType.text_inline),
            ],
        )

    def test_text_to_textnodes_plain_text_only(self):
        text = "This is plain text with no formatting."
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            nodes,
            [
                TextNode("This is plain text with no formatting.", TextType.text_inline),
            ],
        )

    def test_text_to_textnodes_multiple_same_formatting(self):
        text = "This is **bold** and **another bold** text."
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            nodes,
            [
                TextNode("This is ", TextType.text_inline),
                TextNode("bold", TextType.bold_inline),
                TextNode(" and ", TextType.text_inline),
                TextNode("another bold", TextType.bold_inline),
                TextNode(" text.", TextType.text_inline),
            ],
        )

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    def test_block_to_block_type(self):
        self.assertEqual(block_to_block_type("This is a paragraph"), BlockType.paragraph)
        self.assertEqual(block_to_block_type("- This is a list item"), BlockType.unordered_list)
        self.assertEqual(block_to_block_type("1. This is an ordered list item"), BlockType.ordered_list)
        self.assertEqual(block_to_block_type("> This is a quote"), BlockType.quote)
        self.assertEqual(block_to_block_type("```python\nprint('Hello, World!')\n```"), BlockType.code)
        self.assertEqual(block_to_block_type(""), BlockType.paragraph)
        self.assertEqual(block_to_block_type("# Heading"), BlockType.heading)

    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
    )

    def test_heading(self):
        md = "## This is a heading"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h2>This is a heading</h2></div>")

    def test_quote(self):
        md = "> This is a quote\n> with multiple lines"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><blockquote>This is a quote with multiple lines</blockquote></div>")

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
    )

    def test_unordered_list(self):
        md = "- item one\n- item two"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><ul><li>item one</li><li>item two</li></ul></div>")

    def test_ordered_list(self):
        md = "1. item one\n2. item two"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><ol><li>item one</li><li>item two</li></ol></div>")

    def test_markdown(self):
        test_md = "Here's what `elflang` looks like (the perfect coding language):"
        node = markdown_to_html_node(test_md)
        print(node.to_html())

    def test_img(self):
        md = "![JRR Tolkien sitting](/images/tolkien.png)"
        node = markdown_to_html_node(md)
        print(node.to_html())