import os
import sys
from ebooklib import epub
import ebooklib
from bs4 import BeautifulSoup
import math
import re

def bionic_reading(text):
    num_chars = math.ceil(len(text)/2)
    return '<b>' + text[:num_chars] + '</b>' + text[num_chars:]


def modify_html(html_content):
    soup = BeautifulSoup(html_content, "html.parser")

    for text_node in soup.find_all(text=True):
        if text_node.parent.name not in ['style', 'script', 'head', 'title', 'meta', '[document]']:
            new_text = ' '.join([bionic_reading(word) for word in text_node.split()])
            if text_node[-1] == " ":
                new_text += " "
            elif text_node[0] == " ":
                new_text = " " + new_text
            new_text = " " + new_text
            new_text = new_text + " "
            new_text = re.sub(r"\s+", " ", new_text)
            text_node.replace_with(BeautifulSoup(new_text, "html.parser"))

    return str(soup)

def modify_epub(input_file, output_file):
    book = epub.read_epub(input_file)

    styles = book.get_items_of_type(ebooklib.ITEM_STYLE)
    styles_list = []
    
    for style in styles:
        style_item = book.get_item_with_href(style.get_name())
        styles_list.append(style_item)

    for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
        for style in styles_list:
            item.add_link(href=style.get_name(), rel="stylesheet", type="text/css")

        modified_content = modify_html(item.content.decode())
        item.content = modified_content.encode('utf-8')

    epub.write_epub(output_file, book)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python bionic.py input_file.epub output_file.epub")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    if not os.path.exists(input_file):
        print(f"Error: {input_file} does not exist.")
        sys.exit(1)

    modify_epub(input_file, output_file)
    print(f"Modified EPUB file saved as {output_file}.")