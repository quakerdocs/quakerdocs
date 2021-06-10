# TODO maybe change page, count to data for easier expansion.

import re
import nltk
import json
import struct
from collections import Counter
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

try:
    stopwords = set(stopwords.words('english'))
except LookupError:
    nltk.download('stopwords')
    stopwords = set(stopwords.words('english'))


class Trie:
    """
    A class to represent a Radix tree/trie

    Attributes:
        char (string): The string connecting the node to its parent.
        end  (bool): Signifies wether node is an endpoint.
        children (dict): A dictionary connecting chars to child nodes.
        page_count ([(int, int)]): A list of page indexes and word counts.
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
        self.page_count = []

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
            match, rem, word = self.match(c_word, word)

            # Exact match to start of word.
            if not rem:
                # Move a layer deeper.
                return word, child

            # Not exact but still partial match.
            if match:
                # Create a new node for the partial match.
                new = Trie(match)

                # Update the char of the child and move it the new node.
                child.char = c_rem
                new.children[c_rem] = child
                current.children.pop(c_word)
                current.children[match] = new

                # Continue after the partial match.
                if word:
                    # Create the remaining word object below.
                    current = new
                    break
                else: # The word fits in the new node.
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
        current.page_count.append((page, count))

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
                i -= 1
                break

        i += 1

        # Return matching part and both remainders.
        return n_word[:i], n_word[i:], s_word[i:]

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
            for key, child in node.children.items(): #sorted(node.children.items(), key=lambda c: c[0]):
                child.key = key
                node.sorted_children.append(child)

            # Update the stack and the counts.
            stack.extend(reversed(node.sorted_children))
            children_count += len(node.children)
            pages_count += len(node.page_count)
            char_count += len(node.char) + 1

        # Convert the radix trie to byte data.
        node_arr, children_arr, page_arr, char_arr = [], [], [], []
        char_len = 0

        # Add each node to the binary arrays.
        for node in nodes:
            node_arr += struct.pack('IIIII', char_len,
                                    len(children_arr) // 4,
                                    len(page_arr) // 4,
                                    len(node.children),
                                    len(node.page_count))
            children_i = [child.i for child in node.sorted_children]
            children_arr += struct.pack('I' * len(children_i), *children_i)
            pages = [i for p in node.page_count for i in p]
            page_arr += struct.pack('H' * len(pages), *pages)
            char_arr += ['"'] + list(node.char) + ['\\0"']
            char_len += len(node.char) + 1

        # Convert the data to C arrays.
        return {
            'node_arr': ','.join(map(str, node_arr)),
            'children_arr': ','.join(map(str, children_arr)),
            'page_arr': ','.join(map(str, page_arr)),
            'char_arr': ''.join(char_arr)
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
        self.urltitles = []   # [(url, title), ...]
        self.trie = Trie("")  # root of the prefix trie

        self.stemmer = SnowballStemmer(language="english").stem
        self.remover = re.compile('[^\\w\\s]')

        self.wordset = set()

    def parse_file(self, content, title, url):
        """
        Add a file to the index.

        :param list content: A list of lowercase words from the file
        :param str title: The title of the document
        :param str url: The url of the page
        """

        # Change to lowercase, separate _ and only keep letters/numbers.
        content = content.lower().replace('_', '')
        content = self.remover.sub('', content)

        # Remove stopwords.
        content = [self.stemmer(word)
                   for word in content.split() if word not in stopwords]

        # Count occurences of words in page.
        word_counter = Counter(content)

        # Get the index of the current page and update the list.
        i = len(self.urltitles)
        self.urltitles.append((url, title))

        # Create the trie.
        for word, count in sorted(word_counter.items(), key=lambda x: x[1]):
            self.trie.insert(word, i, count)
            self.wordset.add(word)

    def to_json(self):
        """
        Return a json string containing the index and a mapping from ids to
        tuples of (url, title).
        """
        self.optimise()
        return json.dumps(self.urltitles), json.dumps(self.trie)

    def to_binary(self):
        # print(self.trie.children)

        # current = self.trie
        # while word:
        #     word, current = self.scan_children(word, current)

        # # If while loop exited it means that the current node is an end node.
        # current.end = True
        # current.page_count.append((page, count))

        stack = [self.trie]

        def doPrint(node, pre):
            total = 0
            if node.end:
                total += 1
                print(pre + node.char)
            for child in node.children.values():
                total += doPrint(child, pre + node.char)
            return total

        print(self.wordset)
        print("wordcount: ", doPrint(self.trie, ""))
        print('count', len(self.wordset))
        # while stack:
        #     node = stack.pop()
        #     print(node.char)
        #     stack.extend(node.children.values())

        binar = self.trie.to_binary()


        return binar
