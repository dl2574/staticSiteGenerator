import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

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


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "This Link", {"href":"www.google.com"})
        self.assertEqual(node.to_html(), "<a href=\"www.google.com\">This Link</a>")

    def test_leaf_to_html_b(self):
        node = LeafNode("b", "BOLD TEXT")
        self.assertEqual(node.to_html(), "<b>BOLD TEXT</b>")


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_error_with_no_children(self):
        parent_node = ParentNode("div", None)
        self.assertRaises(ValueError, parent_node.to_html)

    def test_error_with_no_tag(self):
        parent_node = ParentNode(None, None)
        self.assertRaises(ValueError, parent_node.to_html)