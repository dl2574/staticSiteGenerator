import re

from textnode import TextNode, TextType
from htmlnode import LeafNode

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, value=text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src":text_node.url, "alt":text_node.text})

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_node_list = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            split_node = node.text.split(delimiter)
            for i, text in enumerate(split_node):
                if i % 2 == 0:
                    new_node_list.append(TextNode(text,TextType.TEXT))
                else:
                    new_node_list.append(TextNode(text, text_type))
        else:
            new_node_list.append(node)

    return new_node_list

def extract_markdown_images(text):
    matches = re.findall(r"\!\[(.*?)\]\((.*?)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r" \[(.*?)\]\((.*?)\)", text)
    return matches

def split_nodes_image(old_nodes):
    new_node_list = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            extracted_images = extract_markdown_images(node.text)
            split_node = re.split(r"\!\[.*?\]\(.*?\)", node.text)
            for text in split_node:
                if text == "":
                    try:
                        image = extracted_images.pop(0)
                        new_node_list.append(TextNode(image[0], TextType.IMAGE, image[1]))
                    except IndexError:
                        pass

                else:
                    new_node_list.append(TextNode(text, TextType.TEXT))
                    try:
                        image = extracted_images.pop(0)
                        new_node_list.append(TextNode(image[0], TextType.IMAGE, image[1]))
                    except IndexError:
                        pass
        else:
            new_node_list.append(node)
    return new_node_list



def split_nodes_link(old_nodes):
    new_node_list = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            extracted_links = extract_markdown_links(node.text)
            split_node = re.split(r"\[.*?\]\(.*?\)", node.text)
            for text in split_node:
                if text == "":
                    try:
                        link = extracted_links.pop(0)
                        new_node_list.append(TextNode(link[0], TextType.LINK, link[1]))
                    except IndexError:
                        pass

                else:
                    new_node_list.append(TextNode(text, TextType.TEXT))
                    try:
                        link = extracted_links.pop(0)
                        new_node_list.append(TextNode(link[0], TextType.LINK, link[1]))
                    except IndexError:
                        pass
        else:
            new_node_list.append(node)
    return new_node_list

def text_to_textnodes(text):
    base_node = TextNode(text, TextType.TEXT)
    bold_list = split_nodes_delimiter([base_node], "**", TextType.BOLD)
    bold_italic_list = split_nodes_delimiter(bold_list, "_", TextType.ITALIC)
    bold_italic_code_list = split_nodes_delimiter(bold_italic_list, "`", TextType.CODE)
    bold_italic_code_image_list = split_nodes_image(bold_italic_code_list)
    final_list = split_nodes_link(bold_italic_code_image_list)
    return final_list
