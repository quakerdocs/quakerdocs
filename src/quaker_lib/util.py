"""
Utility file containing useful functionality for throughout the project.
"""

import re

# From https://github.com/sphinx-doc/sphinx/blob/4.x/sphinx/util/nodes.py
_explicit_title_re = re.compile(r'^(.+?)\s*(?<!\x00)<([^<]*?)>$', re.DOTALL)


def link_explicit(link):
    """
    Check whether the link format is a 'explicit link' in the format of:
    Link Title <link_ref>
    If this is the case, return tuple (Title, Reference).
    Otherwise return None.
    """
    res = _explicit_title_re.match(link)
    if res:
        return (res.group(1), res.group(2))

    return None