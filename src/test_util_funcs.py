import unittest
import utils

from textnode import TextNode, TextType
from blocknode import BlockType


class TestTextToHTMLFunc(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = utils.text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")


class TestSplitNodeDelimiterFunc(unittest.TestCase):
    def test_code_split(self):
        node = TextNode("This is a piece of text with a `code block` in it.", TextType.TEXT)
        new_nodes = utils.split_nodes_delimiter([node], "`", TextType.CODE)
        expected_result = [
            TextNode("This is a piece of text with a ", TextType.TEXT), 
            TextNode("code block", TextType.CODE), 
            TextNode(" in it.", TextType.TEXT)
            ]
        self.assertIsInstance(new_nodes,list)
        self.assertEqual(new_nodes, expected_result)

    def test_bold_split(self):
        node = TextNode("This is a piece of text with **BOLD TEXT** in it.", TextType.TEXT)
        new_nodes = utils.split_nodes_delimiter([node], "**", TextType.BOLD)
        expected_result = [
            TextNode("This is a piece of text with ", TextType.TEXT), 
            TextNode("BOLD TEXT", TextType.BOLD), 
            TextNode(" in it.", TextType.TEXT)
            ]
        self.assertIsInstance(new_nodes,list)
        self.assertEqual(new_nodes, expected_result)
    
    def test_multiple_code_split(self):
        node = TextNode("This is a piece of text with two `code` `blocks` in it.", TextType.TEXT)
        new_nodes = utils.split_nodes_delimiter([node], "`", TextType.CODE)
        expected_result = [
            TextNode("This is a piece of text with two ", TextType.TEXT), 
            TextNode("code", TextType.CODE),
            TextNode(" ", TextType.TEXT),
            TextNode("blocks", TextType.CODE),
            TextNode(" in it.", TextType.TEXT)
            ]
        self.assertIsInstance(new_nodes,list)
        self.assertEqual(new_nodes, expected_result)
        
class TestExtractImage(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = utils.extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_does_not_match_link(self):
        matches = utils.extract_markdown_images(
            "This is text with an [Link](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertEqual(matches, [])

class TestExtractLink(unittest.TestCase):
    def test_extract_markdown_link(self):
        matches = utils.extract_markdown_links(
            "This is text with an [Link](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("Link", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_does_not_match_image(self):
        matches = utils.extract_markdown_links(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertEqual(matches, [])

class TestSplitImageNodes(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = utils.split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                )
            ],
            new_nodes,
        )

class TestSplitLinkNodes(unittest.TestCase):
    def test_split_links(self):
        node = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = utils.split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                )
            ],
            new_nodes,
        )

class TestTextToTextNodes(unittest.TestCase):
    def test_split_all(self):
        base_text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        node_list = utils.text_to_textnodes(base_text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            node_list
        )

class TestMarkdownToBlocks(unittest.TestCase):
        def test_markdown_to_blocks(self):
            md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
            blocks = utils.markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                [
                    "This is **bolded** paragraph",
                    "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                    "- This is a list\n- with items",
                ],
            )

class TestBlockToBlockType(unittest.TestCase):
    def test_heading_type(self):
        heading_1 = "# Heading"
        heading_2 = "## Heading"
        heading_3 = "### Heading"
        heading_4 = "#### Heading"
        heading_5 = "##### Heading"
        heading_6 = "###### Heading"
        not_heading = "* Heading"

        self.assertEqual(utils.block_to_block_type(heading_1), BlockType.HEADING)
        self.assertEqual(utils.block_to_block_type(heading_2), BlockType.HEADING)
        self.assertEqual(utils.block_to_block_type(heading_3), BlockType.HEADING)
        self.assertEqual(utils.block_to_block_type(heading_4), BlockType.HEADING)
        self.assertEqual(utils.block_to_block_type(heading_5), BlockType.HEADING)
        self.assertEqual(utils.block_to_block_type(heading_6), BlockType.HEADING)
        self.assertNotEqual(utils.block_to_block_type(not_heading), BlockType.HEADING)

    def test_code_block(self):
        code_text = "```Some code...```"
        code_text_with_linebreak = "```Line 1\nLine2```"
        not_code = "``something``"
        not_code2 = "```something without the right end``"
        not_code3 = "``Something without the right start```"

        self.assertEqual(utils.block_to_block_type(code_text), BlockType.CODE)
        self.assertEqual(utils.block_to_block_type(code_text_with_linebreak), BlockType.CODE)
        self.assertNotEqual(utils.block_to_block_type(not_code), BlockType.CODE)
        self.assertNotEqual(utils.block_to_block_type(not_code2), BlockType.CODE)
        self.assertNotEqual(utils.block_to_block_type(not_code3), BlockType.CODE)

    def test_quote(self):
        quote_text = "> The first line\n> Next line\n> and last line"
        not_quote = "> First line\nbut not second\n> Third is though"
        not_quote2 = "> First line is\nSecondline isn't"

        self.assertEqual(utils.block_to_block_type(quote_text), BlockType.QUOTE)
        self.assertNotEqual(utils.block_to_block_type(not_quote), BlockType.QUOTE)
        self.assertNotEqual(utils.block_to_block_type(not_quote2), BlockType.QUOTE)

    def test_unordered_list(self):
        list_text = "- Item one\n- Item two\n- Item three"
        not_list = "- Item 1\nand item 2"
        not_list2 = "- Item 1\nnot 2\n - yes 3"

        self.assertEqual(utils.block_to_block_type(list_text), BlockType.UO_LIST)
        self.assertNotEqual(utils.block_to_block_type(not_list), BlockType.UO_LIST)
        self.assertNotEqual(utils.block_to_block_type(not_list2), BlockType.UO_LIST)

    def test_ordered_list(self):
        list_text = "1. Test list\n2. List item 2\n3. and list item 3"
        not_list = "e. List item 1\n5. item 3\nt. item 3"
        not_list2 = "1. List item 1\n1. List item 2"

        self.assertEqual(utils.block_to_block_type(list_text), BlockType.O_LIST)
        self.assertNotEqual(utils.block_to_block_type(not_list), BlockType.O_LIST)
        self.assertNotEqual(utils.block_to_block_type(not_list2), BlockType.O_LIST)

    def test_paragraph(self):
        p_text = "This is a paragraph"

        self.assertEqual(utils.block_to_block_type(p_text), BlockType.PARAGRAPH)


class MarkdownToHTMLNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = utils.markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = utils.markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
