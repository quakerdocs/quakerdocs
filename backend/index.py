# TODO maybe change page, count to data for easier expansion.
import os
import re
import nltk
import json
import struct
import shutil
from jinja2 import Template
from collections import Counter
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
import math

try:
    stopwords = set(stopwords.words('english'))
except LookupError:
    nltk.download('stopwords')
    stopwords = set(stopwords.words('english'))


class CPrimitive():
    """
    A class to the minimum required primitive data type which can hold an
    integer. This can then be used in C/C++ and with the struct library.

    Attributes:
        actual_bytes (int): The strictly needed bytes for the given size.
        id  (string): The struct library type identifier.
        type (string): The C primitive typename.
        bytes (int): The byte size of the chosen primitive.
    """

    def __init__(self, size: int):
        """
        Choose the minimum required data type based on the size.

        Parameters:
            size (int): An integer containing the maximum value the primitive
            should be able to hold.
        """
        self.actual_bytes = math.ceil(math.log2(size) / 8)

        if self.actual_bytes == 1:
            self.id, self.type, self.bytes = 'B', 'unsigned char', 1
        elif self.actual_bytes == 2:
            self.id, self.type, self.bytes = 'H', 'unsigned short', 2
        elif self.actual_bytes <= 4:
            self.id, self.type, self.bytes = 'I', 'unsigned int', 4
        elif self.actual_bytes <= 8:
            self.id, self.type, self.bytes = 'Q', 'unsigned long long', 8
        else:
            raise ValueError('Too much data in the search index.')


class Trie:
    """
    A class to represent a Radix tree/trie

    Attributes:
        char (string): The string connecting the node to its parent.
        end  (bool): Signifies wether node is an endpoint.
        children (dict): A dictionary connecting chars to child nodes.
        pages ([(int, int)]): A list of page indexes and word counts.
    """

    def __init__(self, char):
        """
        Constructor for the Trie class.

        Parameters:
            char (string): The string connecting the node to its parent.
        """

        # Current character.
        self.char = char

        # Wether at end of word or not.
        self.end = False

        # Dict of children.
        self.children = {}

        # The pages where this word is found.
        self.pages = []

    def insert_helper(self, word, current):
        """
        A helper method used to insert a fragment of a word into the trie.

        Parameters:
            word (string): The remainder of the word to insert a fragment of.
            current (Trie): The node of the trie from which to start searching.
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
                else:  # The word fits in the new node.
                    return "", new

        # If none of the children matched add the remainder as a child.
        new = Trie(word)
        current.children[word] = new
        return "", new

    def insert(self, word, page, count):
        """
        Insert method to insert a new word into the trie.

        Parameters:
            word (string): The word to be inserted.
            page (int): The index of the page the word is in.
            count (int): The number of times the word is found.
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
    def match(n_word, s_word):
        """
        Method to match a part of a word to a part in the node.

        Parameters:
            n_word (string): The word fragment inside the node.
            s_word (string): The fragment of the word being searched.
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

    def to_binary(self):
        """Translate the Trie to a binary format"""
        # Put all the nodes in a list.
        nodes, stack = [], [self]
        char_count, children_count, page_count = 0, 0, 0
        max_children, max_pages = 0, 0
        page_index_max, page_count_max = 0, 0

        while stack:
            node = stack.pop()
            node.i = len(nodes)
            nodes.append(node)
            children_count += len(node.children)
            page_count += len(node.pages)
            char_count += len(node.char) + 1
            max_children = max(max_children, len(node.children))
            max_pages = max(max_pages, len(node.pages))
            stack.extend(reversed(node.children.values()))

            for index, count in node.pages:
                page_index_max = max(page_index_max, index)
                page_count_max = max(page_count_max, count)

        node_p = CPrimitive(len(nodes))
        child_s = CPrimitive(max_children)
        page_s = CPrimitive(max_pages)
        child_p = CPrimitive(children_count)
        page_p = CPrimitive(page_count)
        char_p = CPrimitive(char_count)
        page_i = CPrimitive(page_index_max)
        page_c = CPrimitive(page_count_max)

        # Convert the radix trie to byte data.
        node_arr, children_arr, page_arr, char_arr = [], [], [], []
        char_len = 0

        # Add each node to the binary arrays.
        for node in nodes:
            node_arr += struct.pack(
                char_p.id + child_p.id + page_p.id + child_s.id + page_s.id,
                char_len, len(children_arr) // child_p.bytes,
                len(page_arr) // (page_i.bytes + page_c.bytes),
                len(node.children), len(node.pages))

            # Add the children.
            children_i = [child.i for child in node.children.values()]
            children_arr += struct.pack(node_p.id * len(children_i), *children_i)

            # Add the pages.
            for page in node.pages:
                page_arr += struct.pack(page_i.id + page_c.id, *page)

            # Add the characters.
            char_arr += ['"'] + list(node.char) + ['\\0"']
            char_len += len(node.char) + 1

        # Convert the data to C arrays.
        return {
            'node_arr': ','.join(map(str, node_arr)),
            'children_arr': ','.join(map(str, children_arr)),
            'page_arr': ','.join(map(str, page_arr)),
            'char_arr': ''.join(char_arr),
            'node_p': node_p, 'child_s': child_s, 'page_s': page_s,
            'child_p': child_p, 'page_p': page_p, 'char_p': char_p,
            'page_i': page_i, 'page_c': page_c
        }


class IndexGenerator:
    """
    A class to generate the indexing/trie used for searching as well as the
    translation of page indices to page info.
    """

    def __init__(self):
        """
        Constructor for the IndexGenerator class.
        """
        self.urltitles = []  # [(url, title), ...]
        self.trie = Trie("")  # root of the prefix trie

        self.stemmer = SnowballStemmer(language="english").stem
        self.remover = re.compile('[^\\w\\s\\n]')
        # self.spacer = re.compile('[\._]')

    def parse_file(self, content, title, url):
        """
        Add a file to the index.

        :param list content: A list of lowercase words from the file
        :param str title: The title of the document
        :param str url: The url of the page
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
            self.trie.insert(word, i, count)

    def to_json(self):
        """
        Return a json string containing the index and a mapping from ids to
        tuples of (url, title).
        """
        self.optimise()
        return json.dumps(self.urltitles), json.dumps(self.trie)

    def build(self, dest_path):
        """
        Write the search index file to the destination directory.
        """
        path = os.path.join('backend', 'wasm')

        if not os.path.exists(path):
            raise FileNotFoundError('Wasm source files are not found.')

        # Generate the search.hpp
        data = self.trie.to_binary()
        with open(os.path.join(path, 'search.hpp.jinja')) as f:
            template = Template(f.read())

            # Write the search index to hpp.
            with open(os.path.join(path, 'search.hpp'), 'w') as f:
                f.write('/*=== AUTOMATICALLY GENERATED FILE ===*/\n\n')
                f.write(template.render(urltitles=self.urltitles, **data))

        # Make the .wasm file
        working_dir = os.getcwd()
        os.chdir(path)
        os.system('make')
        os.chdir(working_dir)

        if not os.path.exists(dest_path):
            os.mkdir(dest_path)

        shutil.copyfile(os.path.join(path, 'build', 'search_data.js'),
                        os.path.join(dest_path, 'search_data.js'))
        shutil.copyfile(os.path.join(path, 'build', 'search_data.wasm'),
                        os.path.join(dest_path, 'search_data.wasm'))
