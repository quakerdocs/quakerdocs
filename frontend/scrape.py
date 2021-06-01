"""
This script scrapes the HTML files created by sphinx-build that are stored in
the HTML_SRC.
"""

from bs4 import BeautifulSoup
import os

# Root is parent folder of python folder.
ROOT = os.getcwd().replace('python', '')
HTML_SRC = ROOT + "/src_pages"
HTML_DST = ROOT + "/"
HTML_TEMPLATE = "index.html"

def get_html_src_files(path=HTML_SRC):
    files = os.listdir(HTML_SRC)
    return list(files)

def read_file(filename, is_source=True):
    path = HTML_SRC if is_source else ROOT
    with open(f"{path}/{filename}", 'r') as f:
        return f.read()

def write_file(filename, content):
    with open(f"{HTML_DST}/{filename}", 'w+') as f:
        f.write(content)

def transfer_html_data(filename, template_file=HTML_TEMPLATE):
    src_doc = read_file(filename)
    template_doc = read_file(template_file, False)

    new_content = scrape_and_merge(src_doc, template_doc)
    write_file(filename, new_content)

def scrape_and_merge(src_doc, template_doc):
    src_soup = BeautifulSoup(src_doc, 'html.parser')
    template_soup = BeautifulSoup(template_doc, 'html.parser')

    content = src_soup.select('div.section')[0]
    template_soup.html.select('div#content')[0].append(content)

    navigation = src_soup.select('li.toctree-l1')

    return str(template_soup.prettify())


def main():
    src_files = get_html_src_files()

    for src_file in src_files:
        transfer_html_data(src_file)

if __name__ == "__main__":
    main()

