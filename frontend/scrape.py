"""
This script scrapes the HTML files created by sphinx-build that are stored in
the HTML_SRC.
"""

from bs4 import BeautifulSoup
import os
import re

# Root is parent folder of python folder.
ROOT = os.getcwd().replace('python', '')
HTML_SRC = ROOT + "/src_pages"
HTML_DST = ROOT + "/gen_pages"
HTML_TEMPLATE = "/templates/template.html"


def get_html_src_files(path=HTML_SRC):
    """
    Retrieve all files in the given HTML source path.
    """
    files = os.listdir(HTML_SRC)
    return list(files)


def read_file(filename, is_source=True):
    """
    Read all data in filename, in the HTML source directory if is_source is
    True, in the ROOT directory otherwise.
    """
    path = HTML_SRC if is_source else ROOT
    with open(f"{path}/{filename}", 'r') as f:
        return f.read()


def write_file(filename, content):
    """
    Write content to filename in the destination HTML directory.
    """
    with open(f"{HTML_DST}/{filename}", 'w+') as f:
        f.write(content)


def transfer_html_data(filename, template_file=HTML_TEMPLATE):
    """
    Transfer all necessary HTML data from filename to template_file.
    """
    src_doc = read_file(filename)
    template_doc = read_file(template_file, False)

    new_content = scrape_and_merge(src_doc, template_doc)
    write_file(filename, new_content)


def scrape_and_merge(src_doc, template_doc):
    """
    Retrieve the data from the HTML section in src_doc and paste it into a copy
    template_doc.
    """

    src_soup = BeautifulSoup(src_doc, 'html.parser')
    template_soup = BeautifulSoup(template_doc, 'html.parser')

    # Add the title of the src_doc to template_doc.
    title = src_soup.find('title').contents[0]
    print(title)
    template_soup.html.select('title')[0].append(title)
    template_soup.html.select('h1.title')[0].append(title.split('—')[1][1:])

    print("\n")
    # Retrieve the id of the content div/section
    regex = re.compile('[^a-zA-Z -]')
    regID = regex.sub('', title.split('—')[0][:-1])
    contentID = regID.replace(' ', '-').lower()
    # print(contentID)
    # Add the main page content from src_doc to template_doc.
    content = src_soup.select('#' + contentID)[0]
    content['class'] = content.get('class', []) + ["section"]

    sidebar = src_soup.select('div.sphinxsidebarwrapper')[0]

    for el in sidebar:
        if el.name == 'p':
            el['class'] = el.get('class', []) + ['menu-label']
        elif el.name == 'ul':
            el['class'] = el.get('class', []) + ['menu-list']

    template_soup.html.select('div#content')[0].append(content)
    template_soup.html.select('aside#menuPanel')[0].append(sidebar)

    return str(template_soup.prettify())


def main():
    src_files = get_html_src_files()

    for src_file in src_files:
        transfer_html_data(src_file)

    # create_sidebar_file(src_file, "sidebar.html")


if __name__ == "__main__":
    main()
