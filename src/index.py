""" Module to generate a radix prefix trie and a list of page info.

This module implements a radix prefix trie class that only contains methods
to add new words to the trie or to store the contents of the trie in a binary
representation. A class is also implemented to find the minimum sized data type
that is able to store a given integer using the struct library. Lastly there
is also a class that can parse a block of text and create a hpp file containing
the resulting trie and page infos.

Notes
-----
When this module is loaded it checks wheter or not the english stopwords are
available on the machine and downloads them if they are not available.

Attributes
----------
stopwords : set
    A set of stopwords used in the english language and should be removed.

"""

import os
import re
import math
import struct
from pathlib import Path
from typing import Tuple
from jinja2 import Template
from collections import deque
from collections import Counter
from nltk.corpus import stopwords
from types import SimpleNamespace

try:
    stopwords = set(stopwords.words('english'))
except LookupError:
    from nltk import download
    download('stopwords')
    stopwords = set(stopwords.words('english'))


def get_primitive(size: int) -> SimpleNamespace:
    """Choose the minimum required data type based on the size.

    Parameters
    ----------
    size : int
        The maximum value the primitive should be able to hold.

    Raises
    ------
    ValueError
        When there is too much data in the index.

    Returns
    -------
    SimpleNamespace
        An object containing the id, type and number of bytes.

    """
    prim = SimpleNamespace()
    prim.actual_bytes = math.ceil(math.log2(size) / 8)

    if prim.actual_bytes == 1:
        prim.id, prim.type, prim.bytes = 'B', 'unsigned char', 1
    elif prim.actual_bytes == 2:
        prim.id, prim.type, prim.bytes = 'H', 'unsigned short', 2
    elif prim.actual_bytes <= 4:
        prim.id, prim.type, prim.bytes = 'I', 'unsigned int', 4
    elif prim.actual_bytes <= 8:
        prim.id, prim.type, prim.bytes = 'Q', 'unsigned long long', 8
    else:
        raise ValueError('Too much data in the search index.')

    return prim


class Trie:
    """A class to represent a Radix tree/trie.

    Attributes
    ----------
    char : str
        The string connecting the node to its parent.
    end : bool
        Signifies wether node is an endpoint.
    children : dict
        A dictionary connecting chars to child nodes.
    pages : [(int, int)]
        A list of page indexes and word counts.

    """

    def __init__(self, char: str):
        """Constructor for the Trie class.

        Parameters
        ----------
        char : str
            The string connecting the node to its parent.

        """

        # Current character.
        self.char = char

        # Wether at end of word or not.
        self.end = False

        # Dict of children.
        self.children = {}

        # The pages where this word is found.
        self.pages = []

    def insert_helper(self, word: str, current: "Trie") -> Tuple[str, "Trie"]:
        """A helper method used to insert a fragment of a word into the trie.

        Parameters
        ----------
        word : str
            The remainder of the word to insert a fragment of.
        current : Trie
            The node of the trie from which to start searching.

        Returns
        -------
        str
            The remaining part of the word, can be empty.
        Trie
            The last node where a string was inserted.

        """

        # Loop over the children of the current node.
        for c_word, child in current.children.items():
            # Find how well the current node matches the word.
            match, remainder, word = self.match(c_word, word)

            # Exact match to start of word.
            if not remainder:
                # Move a layer deeper.
                return word, child

            # Not exact but still partial match.
            if match:
                # Create a new node for the partial match.
                new = Trie(match)

                # Update the char of the child and move it the new node.
                child.char = remainder
                new.children[remainder] = child
                current.children.pop(c_word)
                current.children[match] = new

                # Continue after the partial match.
                if word:
                    # Create the remaining word object below.
                    current = new
                    break
                # The word fits in the new node.
                return "", new

        # If none of the children matched add the remainder as a child.
        new = Trie(word)
        current.children[word] = new
        return "", new

    def insert(self, word: str, page: int, count: int):
        """Insert method to insert a new word into the trie.

        Parameters
        ----------
        word : str
            The word to be inserted.
        page : int
            The index of the page the word is in.
        count : int
            The number of times the word is found.

        """
        if not word:
            return

        # Start at the root.
        current = self

        # Continue until the end of the word.
        while word:
            word, current = self.insert_helper(word, current)

        # If while loop exited it means that the current node is an end node.
        current.end = True
        current.pages.append((page, count))

    @staticmethod
    def match(n_word: str, s_word: str):
        """Method to match a part of a word to a part in the node.

        Parameters
        ----------
        n_word : str
            The word fragment inside the node.
        s_word : str
            The fragment of the word being searched.

        Returns
        -------
        str
            The matching part of the words.
        str
            The remaining part of n_word.
        str
            The remaining part of s_word.

        """

        # Loop over both words.
        for i, (n_char, s_char) in enumerate(zip(n_word, s_word)):
            # Stop on first difference.
            if n_char != s_char:
                break
        else:
            i += 1

        # Return matching part and both remainders.
        return n_word[:i], n_word[i:], s_word[i:]

    def flatten_data(self) -> SimpleNamespace:
        """ Convert the trie to an object containing arrays instead of a tree.

        Returns
        -------
        SimpleNamespace
            An object containging the data from the trie as separate arrays.

        """
        # Flatten the node trie into a list.
        data = SimpleNamespace()
        nodes = []

        data.page_p, data.char_p = 0, 0
        data.child_s, data.page_s = 0, 0
        data.page_i, data.page_c = 0, 0

        # Iterate over all the nodes.
        queue = deque([[self]])
        while queue:
            # Get the node and continue iterating over the children.
            node = queue[0].pop()
            if not queue[0]:
                queue.popleft()

            # Convert the children dictionary to a list, and traverse it later.
            node.children_list = list(node.children.values())
            if node.children_list:
                queue.append(list(reversed(node.children_list)))

            # Append the node to the node list.
            node.i = len(nodes)
            nodes.append(node)

            # Count the number of children, pages and characters.
            data.page_p += len(node.pages)
            data.char_p += len(node.char) + 1  # + 1 for '\0'.

            # Get the highest number of children / pages.
            data.child_s = max(data.child_s, len(node.children))
            data.page_s = max(data.page_s, len(node.pages))

            # Get the highest page index / page count in a node.
            for index, count in node.pages:
                data.page_i = max(data.page_i, index)
                data.page_c = max(data.page_c, count)

        # Get the minimum primitive data type for each of the values.
        for key, val in data.__dict__.items():
            setattr(data, key, get_primitive(val))

        # Get the smallest size primitives which can store the found values.
        data.nodes = nodes
        data.node_p = get_primitive(len(nodes))

        return data

    def to_binary(self):
        """Translate the Trie to a binary format

        Returns
        -------
        Dict
            The binary representations of the radix trie.

        """
        # Put all the nodes in a list.
        t = self.flatten_data()

        # Convert the radix trie to byte data.
        node_arr, page_arr, char_arr = [], [], []
        char_len = 0

        # Add each node to the binary arrays.
        for node in t.nodes:
            struct_format = (t.char_p.id + t.node_p.id + t.page_p.id
                             + t.child_s.id + t.page_s.id)

            # Add the node data.
            node_arr += struct.pack(
                struct_format,
                char_len,
                node.children_list[0].i if node.children else 0,
                len(page_arr) // (t.page_i.bytes + t.page_c.bytes),
                len(node.children), len(node.pages)
            )

            # Add the pages.
            for page in node.pages:
                page_arr += struct.pack(t.page_i.id + t.page_c.id, *page)

            # Add the characters.
            char_arr += ['"'] + list(node.char) + ['\\0"']
            char_len += len(node.char) + 1

        # Convert the data to C arrays.
        t.node_arr = ','.join(map(str, node_arr))
        t.page_arr = ','.join(map(str, page_arr))
        t.char_arr = ''.join(char_arr)

        return t


class IndexGenerator:
    """
    A class to generate the indexing/trie used for searching as well as the
    translation of page indices to page info.

    Attributes
    ----------
    urltitles : [(str, str)]
        A list of urls and titles of the pages.
    trie : Trie
        A radix trie to store the words.
    remover
        Regex to match only letters and numbers.

    """

    def __init__(self):
        """Constructor for the IndexGenerator class."""

        self.urltitles = []  # [(url, title), ...]
        self.trie = Trie("")  # root of the prefix trie
        self.remover = re.compile('[^\\w\\s\\n]')

    def add_file(self, content: list, title: str, url: str,
                 priority: float = 1.0):
        """Add a file to the index.

        Parameters
        ----------
        content : list
            A list of words from the file.
        title : str
            The title of the document.
        url : str
            The url of the page.

        """

        # Change to lowercase, separate _ and only keep letters/numbers.
        content = content.lower().replace('_', ' ').replace('.', ' ')
        content = self.remover.sub('', content)

        # Remove stopwords.
        content = [word for word in content.split() if word not in stopwords]

        # Count occurrences of words in page.
        word_counter = Counter(content)

        # Get the index of the current page and update the list.
        i = len(self.urltitles)
        self.urltitles.append((url, title))

        # Create the trie.
        for word, count in sorted(word_counter.items(), key=lambda x: x[1]):
            self.trie.insert(word, i, int(count * priority))

    def build(self, build_path: Path, dest_path: Path):
        """Write the search index file to the destination directory.

        Parameters
        ----------
        build_path : str
            Where to put compile output.
        dest_path : str
            Where to copy the javascript and webassembly files.

        """
        print('Building the search index assembly')
        source_path = Path('src') / 'wasm'

        if not source_path.exists():
            raise FileNotFoundError('Wasm source files are not found.')

        # Generate the search.hpp
        data = self.trie.to_binary()
        with open(source_path / 'search.hpp.jinja') as f:
            template = Template(f.read())

        # Write the search index to hpp.
        search_path = build_path / 'search'
        search_path.mkdir(parents=True, exist_ok=True)
        with open(search_path / 'search.hpp', 'w') as f:
            f.write('/*=== AUTOMATICALLY GENERATED FILE ===*/\n\n')
            f.write(template.render(urltitles=self.urltitles, **data.__dict__))

        # Create the build command.
        emcc = Path('emsdk') / 'upstream' / 'emscripten' / 'emcc'
        cmnd = [f'{emcc}', '-std=c++17', '-flto',
                '-I', f'"{search_path}/"',
                f"{source_path / 'search.cpp'}",
                '-o', f"{dest_path / 'search_data.js'}",
                '-s', 'WASM=1',
                '-s', 'EXPORTED_FUNCTIONS=["_performSearch","_getSearch"]',
                '-s', 'EXPORTED_RUNTIME_METHODS=\'["ccall","cwrap"]\'']

        dest_path.mkdir(parents=True, exist_ok=True)
        os.system(' '.join(cmnd))