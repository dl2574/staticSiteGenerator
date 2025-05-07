import unittest
import utils

from textnode import TextNode, TextType


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