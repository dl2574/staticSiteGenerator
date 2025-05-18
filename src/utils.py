import re
import functools

from textnode import TextNode, TextType
from htmlnode import LeafNode, ParentNode
from blocknode import BlockType

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

def markdown_to_blocks(markdown):
    block_split = markdown.split("\n\n")
    strip_blocks = list(map(lambda s: s.strip(), block_split))
    remove_empty_blocks = [x for x in strip_blocks if x != ""]
    return remove_empty_blocks

def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if block[0:3] == "```" and block[-3:] == "```":
        return BlockType.CODE
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UO_LIST
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.O_LIST
    return BlockType.PARAGRAPH


def find_heading_level(text):
    heading_level = 0

    while heading_level < 6:
        if text[heading_level] == "#":
            heading_level += 1
        else:
            break
    return heading_level

def text_to_children(block_text, block_type):
    process_text = []

    match block_type:
        case BlockType.PARAGRAPH:
            process_text = [block_text]

        case BlockType.HEADING:
            heading_level = find_heading_level(block_text)
            process_text = [block_text[(heading_level+1):]]

        case BlockType.CODE:
            process_text = [block_text.strip("```")]

        case BlockType.QUOTE:
            split_block_text = block_text.split("\n")

            # Remove "> " from the start of each line
            process_text = [item[2:] for item in split_block_text if item != ""]

        case BlockType.UO_LIST:
            split_block_text = block_text.split("\n")

            # Remove "- " from the start of each line
            process_text = [item[2:] for item in split_block_text if item != ""]

        case BlockType.O_LIST:
            split_block_text = block_text.split("\n")

            # Remove "#. " from the start of each line
            process_text = [item[3:] for item in split_block_text if item != ""]

    if len(process_text) > 1:
        child_list = []
        for text in process_text:
            child_nodes = text_to_textnodes(text)
            html_nodes = list(map(text_node_to_html_node, child_nodes))
            child_list.append(html_nodes)
        return child_list
    else:
        child_nodes = text_to_textnodes(process_text[0])
        child_html_nodes = list(map(text_node_to_html_node, child_nodes))
        return [child_html_nodes]



def markdown_to_html_node(markdown):
    text_blocks = markdown_to_blocks(markdown)
    header_node = ParentNode("header", [])
    body_node_children = [header_node]

    
    for block in text_blocks:
        # Determine the type of block
        block_type = block_to_block_type(block)

        # Get a list of lists of child nodes
        child_nodes = text_to_children(block, block_type)

        if (block_type == BlockType.O_LIST) or (block_type == BlockType.UO_LIST):
            list_items = []
            for child_list in child_nodes:
                new_li = ParentNode("li", child_list)
                list_items.append(new_li)
            list_parent = ParentNode(block_type, list_items)
            div_wrap = ParentNode("div", list_parent)
            body_node_children.append(div_wrap)
        elif block_type == BlockType.HEADING:
            hdg_level = find_heading_level(block)
            hdg_parent = ParentNode(f"h{hdg_level}", child_nodes[0])
            div_wrap = ParentNode("div", hdg_parent)
            body_node_children.append(div_wrap)
        elif block_type == BlockType.CODE:
            code_node = ParentNode("code", child_nodes[0])
            pre_wrap = ParentNode("pre", code_node)
            div_wrap = ParentNode("div", pre_wrap)
            body_node_children.append(div_wrap)
        else:
            new_node = ParentNode(block_type, child_nodes[0])
            div_wrap = ParentNode("div", new_node)
            body_node_children.append(div_wrap)


    body_node = ParentNode("body", body_node_children)
    html_node = ParentNode("html", [body_node])
    return html_node
