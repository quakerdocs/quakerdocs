import re
import nltk
import json
import struct
import string
import doctest
from collections import Counter
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

try:
    stopwords = set(stopwords.words('english'))
except LookupError:
    nltk.download('stopwords')
    stopwords = set(stopwords.words('english'))


class Trie:
    def __init__(self, char):
        # Current character.
        self.char = char

        # Wether at end of word or not.
        self.end = False

        # Dict of children.
        self.children = {}

        # The pages where this word is found.
        self.page_count = []

    def scan_children(self, word, current):
        # Loop over the children of the current node.
        for c_word, child in current.children.items():
            # Find how well the current node matches the word.
            match, c_rem, word = self.match(c_word, word)

            # Exact match to start of word.
            if not c_rem:
                # Move a layer deeper.
                return word, child

            # Not exact but still partial match.
            if match:
                # Create a new node for the partial match and add.
                new = Trie(match)
                current.children[match] = new

                # Update the char of the child.
                child.char = c_rem

                # Move the current child to the new node.
                new.children = {c_rem: child}
                del current.children[c_word]

                # Continue after the partial match.
                current = new
                break

        # If none of the children matched add the remainder as a child.
        new = Trie(word)
        current.children[word] = new
        return word, new

    def insert(self, word, page, count):
        if not word:
            return

        # Start at the root.
        current = self

        # https://leetcode.com/problems/implement-trie-prefix-tree/discuss/653851/python-radix-tree-memory-efficient

        # Continue until the end of the word.
        while word:
            word, current = self.scan_children(word, current)


        # If while loop exited it means that the current node is an end node.
        current.end = True
        current.page_count.append((page, count))
        return

    @staticmethod
    def match(n_word, s_word):
        for i, (n_char, s_char) in enumerate(zip(n_word, s_word)):
            if n_char != s_char:
                break
        return n_word[:i], n_word[i:], s_word[i:]

    # def optimise(self):
    #     """Turn this Trie into a Radix Trie"""
    #     stack = [self]
    #     while stack:
    #         node = stack.pop()

    #         while len(node.children) == 1:
    #             child = node.children[0]

    #             node.children = child.children
    #             node.char += child.char
    #             node.end = child.end
    #             node.page_count = child.page_count

    #         stack.extend(node.children.values())

    def to_binary(self):
        """Translate the Trie to a binary format"""
        nodes = []
        char_count, children_count, pages_count = 0, 0, 0

        # Put all the nodes in a list.
        stack = [self]
        while stack:
            node = stack.pop()
            node.i = len(nodes)
            nodes.append(node)

            # Sort the children alphabetically based on the key.
            node.sorted_children = []
            for key, child in sorted(node.children.items(), key=lambda c: c[0]):
                child.key = key
                node.sorted_children.append(child)

            # Update the stack and the counts.
            stack.extend(reversed(node.children.values()))
            children_count += len(node.children)
            pages_count += len(node.page_count)
            char_count += len(node.char) + 1

        # Convert the radix trie to byte data.
        node_arr, children_arr, page_arr, char_arr = [], [], [], []

        # Add each node to the binary arrays.
        for node in nodes:
            node_arr += struct.pack('IIIII', len(char_arr),
                                    len(node.children), len(children_arr),
                                    len(node.page_count),
                                    len(page_arr))
            children_i = [child.i for child in node.sorted_children]
            children_arr += struct.pack('I' * len(children_i), *children_i)
            pages = [i for p in node.page_count for i in p]
            page_arr += struct.pack('H' * len(pages), *pages)
            char_arr += list(node.char) + ['\\0']

        # Convert the data to C arrays.
        return {
            'node_arr': ','.join(map(str, node_arr)),
            'children_arr': ','.join(map(str, children_arr)),
            'page_arr': ','.join(map(str, page_arr)),
            'char_arr': ''.join(char_arr)
        }

        # Write the nodes to binary

        #
        # struct Node {
        #     int chars;       // (pointer)
        #     int child_count;
        #     int children;    // (pointer)
        #     int page_count
        #     int pages;       // (pointer)
        #     bool end;
        # };
        #


class IndexGenerator:
    def __init__(self):
        self.urltitles = []  # [(url, title), ...]
        self.trie = Trie("") # root of the prefix trie
        self.stemmer = SnowballStemmer(language="english").stem

        # keep_chars = string.ascii_lowercase + string.digits + '\\s'
        self.remover = re.compile('[^\\w\\s]')

    def parse_file(self, content, title, url):
        """
        Add a file to the index.

        :param list content: A list of lowercase words from the file
        :param str title: The title of the document
        :param str url: The url of the page
        """
        content = content.lower().replace('_', '')
        content = self.remover.sub('', content)

        keep_chars = string.ascii_lowercase + string.digits
        content = [self.stemmer(word)
                   for word in content.split() if word not in stopwords]
        word_counter = Counter(content)

        i = len(self.urltitles)
        self.urltitles.append((url, title))

        for word, count in sorted(word_counter.items(), key=lambda x: x[1]):
            self.trie.insert(word, i, count)


    def to_json(self):
        """
        Return a json string containing the index and a mapping from ids to
        tuples of (url, title).
        """
        self.optimise()
        return json.dumps(self.urltitles), json.dumps(self.trie)

    def to_binary(self):
        return self.trie.to_binary()

# if __name__ == "__main__":
    # doctest.testmod(verbose=True)
    # test()
