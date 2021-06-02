"""
This script scrapes the HTML files created by sphinx-build that are stored in
the HTML_SRC.
"""

from bs4 import BeautifulSoup
import os
import shutil
import re

# Root is parent folder of python folder.
ROOT = os.getcwd().replace('python', '')
HTML_SRC = ROOT + "/src_pages"
HTML_DST = ROOT + "/dist/"
HTML_TEMPLATE = ROOT + "/html/template.html"


def get_html_src_files():
    """
    Retrieve all files in the given HTML source path.
    """
    files = os.listdir()
    return [f for f in files if f.endswith('.html')]


def read_file(filename):
    """
    Read all data in filename, in the HTML source directory if is_source is
    True, in the ROOT directory otherwise.
    """
    with open(filename, 'r') as f:
        return f.read()


def write_file(filename, content):
    """
    Write content to filename in the destination HTML directory.
    """
    with open(filename, 'w+') as f:
        f.write(content)


def transfer_html_data(filename, template_file=HTML_TEMPLATE):
    """
    Transfer all necessary HTML data from filename to template_file.
    """
    src_doc = read_file(filename)
    template_doc = read_file(template_file)

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
    template_soup.html.select('title')[0].append(title)
    # template_soup.html.select('h1.title')[0].append(title.split('—')[1][1:])

    content = src_soup.select('div.bodywrapper')[0]
    template_soup.html.select('div#content')[0].append(content)

    # Scrape and merge navigation sidebar
    sidebar = src_soup.select('div.sphinxsidebarwrapper')[0]
    title = sidebar.h1.a.text
    sidebar.h1.decompose()
    template_soup.html.select('h1.title')[0].append(title)
    sidebar.h3.decompose()
    sidebar.select('div.relations')[0].decompose()

    for el in sidebar:
        if el.name == 'p':
            el['class'] = el.get('class', []) + ['menu-label']
        elif el.name == 'ul':
            el['class'] = el.get('class', []) + ['menu-list']

    template_soup.html.select('aside#menuPanel')[0].append(sidebar)

    return str(template_soup.prettify())


def copy_dir(src_dir, dst_dir):
    if os.path.exists(dst_dir):
        shutil.rmtree(dst_dir)
    shutil.copytree(src_dir, dst_dir)


def main():
    if not os.path.exists(HTML_DST):
        os.mkdir(HTML_DST)

    copy_dir(HTML_SRC, HTML_DST)
    transfer_html_data(HTML_DST + 'index.html')

    dirs = [d for d in os.listdir(HTML_DST) if os.path.isdir(os.path.join(HTML_DST, d))]
    for d in dirs:
        d = os.path.join(HTML_DST, d)
        os.chdir(d)
        src_files = get_html_src_files()

        for src_file in src_files:
            print("Scraping", src_file)
            transfer_html_data(src_file)

    copy_dir(os.path.join(ROOT, 'css'), HTML_DST + 'css')
    copy_dir(os.path.join(ROOT, 'js'), HTML_DST + 'js')


    # create_sidebar_file(src_file, "sidebar.html")


if __name__ == "__main__":
    main()
