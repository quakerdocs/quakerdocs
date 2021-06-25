"""
Utility file containing useful functionality for throughout the project.
"""

import re
from pathlib import Path

# From https://github.com/sphinx-doc/sphinx/blob/4.x/sphinx/util/nodes.py
_explicit_title_re = re.compile(r'^(.+?)\s*(?<!\x00)<([^<]*?)>$', re.DOTALL)

# From Docutils:
# https://github.com/docutils-mirror/docutils/blob/master/docutils/nodes.py
_non_id_chars = re.compile('[^a-z0-9/]+')
_non_id_at_ends = re.compile('^[-0-9]+|-+$')


def link_explicit(link: str):
    """Check whether the link format is a 'explicit link'.

    Explicit links are of the format:
    Link Title <link_ref>
    If this is the case, return tuple (Title, Reference).
    Otherwise return None.
    """
    res = _explicit_title_re.match(link)
    if res:
        title = res.group(1)
        ref = res.group(2)
        return (title, ref)

    return None


# https://stackoverflow.com/questions/4984647/accessing-dict-keys-like-an-attribute
class Config(dict):
    """
    Dictionary that can be accessed using attributes
    """
    def __init__(self, *args, **kwargs):
        """
        Initialize Config
        """
        super(Config, self).__init__(*args, **kwargs)
        self.__dict__ = self


def make_id(ref: str) -> str:
    """Convert a string to an id format."""
    ref_list = ref.split('#')

    for i, ref in enumerate(ref_list):
        ref = str(Path(ref).with_suffix(''))
        ref = ref.lower()
        ref = _non_id_chars.sub('-', ' '.join(ref.split()))
        ref = _non_id_at_ends.sub('', ref)
        ref_list[i] = ref

    return '#'.join(ref_list)
