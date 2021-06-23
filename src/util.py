"""
Utility file containing useful functionality for throughout the project.
"""

import re

# From https://github.com/sphinx-doc/sphinx/blob/4.x/sphinx/util/nodes.py
_explicit_title_re = re.compile(r'^(.+?)\s*(?<!\x00)<([^<]*?)>$', re.DOTALL)


# From Docutils: https://github.com/docutils-mirror/docutils/blob/master/docutils/nodes.py
_non_id_chars = re.compile('[^a-z0-9]+')
_non_id_at_ends = re.compile('^[-0-9]+|-+$')


def link_explicit(link):
    """
    Check whether the link format is a 'explicit link' in the format of:
    Link Title <link_ref>
    If this is the case, return tuple (Title, Reference).
    Otherwise return None.
    """
    res = _explicit_title_re.match(link)
    if res:
        title = res.group(1)
        res = make_id(res.group(2))
        return (title, res)

    return None


def make_id(ref):
    id = ref.lower()
    id = _non_id_chars.sub('-', ' '.join(id.split()))
    id = _non_id_at_ends.sub('', id)
    return id
