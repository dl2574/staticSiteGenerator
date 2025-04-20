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
        