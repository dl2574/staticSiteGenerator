import unittest

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_text_not_eq(self):
        node = TextNode("Some text", TextType.NORMAL)
        node2 = TextNode("Some other text", TextType.NORMAL)
        self.assertNotEqual(node, node2)

    def test_type_not_eq(self):
        node = TextNode("Some text", TextType.NORMAL)
        node2 = TextNode("Some text", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_url_not_eq(self):
        node = TextNode("Some text", TextType.NORMAL)
        node2 = TextNode("Some text", TextType.NORMAL, "https://someurl.com")
        self.assertNotEqual(node, node2)

    def test_url_eq(self):
        node = TextNode("Some text", TextType.NORMAL, "https://someurl.com")
        node2 = TextNode("Some text", TextType.NORMAL, "https://someurl.com")
        self.assertEqual(node, node2)

    
if __name__ == "__main__":
    unittest.main()