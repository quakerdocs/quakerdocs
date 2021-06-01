"""
This script scrapes the HTML files created by sphinx-build that are stored in
the HTML_SRC. TODO: It is used in the Makefile right after the HTML
files are created by sphinx-build.
"""

from bs4 import BeautifulSoup
import os

HTML_SRC = "../src_pages"
HTML_DEST = "../dst_pages"
HTML_TEMPLATE = "../index.html"

def scrape(src_doc, dest_doc):
    src_soup = BeautifulSoup(src_doc, 'html.parser')
    dest_soup = BeautifulSoup(dest_doc, 'html.parser')

    content = src_soup.select('div.section')
    dest_soup.select('div#content').append(content)

    return str(dest_soup)


def write_file(filename, content):
    with open(filename, 'w') as f:
        f.write(content)


def read_file(filename):
    with open(filename, 'r') as f:
        return f.read()


def get_html_files(directory=HTML_SRC):
    files = os.listdir(directory)
    return list(files)


def main():
    files = get_html_files()
    if not os.path.exists(HTML_DEST):
        os.makedirs(HTML_DEST)

    os.chdir(HTML_SRC)
    for f in files:
        src_doc = read_file(f)
        dest_doc = read_file(HTML_TEMPLATE)
        # os.chdir(HTML_DEST)
        new_content = scrape(src_doc, dest_doc)
        write_file(f, new_content)
        # os.chdir(HTML_SRC)


if __name__ == "__main__":
    main()
