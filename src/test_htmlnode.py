import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_prop_string(self):
        node = HTMLNode("p", "Some P text", props={"href":"somelink", "color":"someColor"})
        prop_string = " href=\"somelink\" color=\"someColor\""
        self.assertEqual(node.props_to_html(), prop_string)

    def test_no_props_string(self):
        node = HTMLNode("p", "some text without props")
        prop_string = ""
        self.assertEqual(node.props_to_html(), prop_string)

    def test_to_HTML_Error(self):
        node = HTMLNode("a", "A Link, WOW", props={"href":"https://www.hellowworld.com"})
        self.assertRaises(NotImplementedError, node.to_html)
    