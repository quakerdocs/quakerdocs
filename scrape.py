#!/usr/bin/env python3
"""
This script scrapes the HTML files created by sphinx-build that are stored in
the HTML_SRC and creates a dist directory containing all static resources.
"""

from bs4 import BeautifulSoup
import os
import shutil
import copy

# Root is parent folder of python folder.
ROOT = os.getcwd().replace('python', '')
HTML_SRC = ROOT + "/build/html"
HTML_DST = ROOT + "/dist/"
HTML_TEMPLATE = ROOT + "/frontend/html/template.html"


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
    # If there is no title we are probably not interested in the file.
    title = src_soup.find('title')
    if not title:
        return ''
    template_soup.html.select('title')[0].append(title.contents[0])
    # template_soup.html.select('h1.title')[0].append(title.split('—')[1][1:])

    content = src_soup.select('div.body')[0]
    headerlinks = content.select('a.headerlink')
    for i in headerlinks:
        bookmark = BeautifulSoup("<span class='material-icons'>bookmark_border</span>")
        i.string = ''
        i.insert(3, bookmark.html.span)

    template_soup.html.select('div#content')[0].append(content)



    # Scrape and merge navigation sidebar
    sidebar = src_soup.select('div.sphinxsidebarwrapper')[0]
    title = sidebar.h1.a.text
    sidebar.h1.decompose()
    template_soup.html.select('h1.title')[0].append(title)
    sidebar.h3.decompose()
    sidebar.select('div.relations')[0].decompose()

    searchbox = sidebar.select('div#searchbox')
    if searchbox:
        searchbox[0].decompose()

    for el in sidebar:
        if el.name == 'p':
            el['class'] = el.get('class', []) + ['menu-label']
        elif el.name == 'ul':
            el['class'] = el.get('class', []) + ['menu-list']

    active_a = src_soup.select('a.current')
    if active_a:
        active_a = active_a[0]
        active_a['class'] = active_a.get('class', []) + ['is-active']

    template_soup.html.select('aside#menuPanel')[0].append(copy.copy(sidebar))
    template_soup.html.select('div#mini-menu')[0].append(sidebar)

    return str(template_soup.prettify())


def copy_dir(src_dir, dst_dir):
    if os.path.exists(dst_dir):
        shutil.rmtree(dst_dir)
    shutil.copytree(src_dir, dst_dir)


def main():
    if not os.path.exists(HTML_DST):
        os.mkdir(HTML_DST)

    copy_dir(HTML_SRC, HTML_DST)

    for root, dirs, files in os.walk(HTML_DST):
        path = root.split(os.sep)

        if os.path.basename(root).startswith('_'):
            continue

        for src_file in files:
            if src_file.endswith('.html'):
                path = os.path.join(root, src_file)
                print("Scraping", path)
                transfer_html_data(path)

    copy_dir(os.path.join(ROOT, 'frontend/css'), HTML_DST + 'css')
    copy_dir(os.path.join(ROOT, 'frontend/js'), HTML_DST + 'js')


if __name__ == "__main__":
    main()
