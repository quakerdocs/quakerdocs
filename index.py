import os
import json
import doctest
from collections import Counter, defaultdict
from nltk.corpus import stopwords
import re
import string

stopwords = set(stopwords.words('english'))


class IndexGenerator:
    def __init__(self):
        self.urltitles = []  # [(url, title), ...]
        self.index = defaultdict(list)  # {"word": [(index, freq), ...]}

        keep_chars = string.ascii_lowercase + ' \n'
        print(keep_chars)
        remove_chars = ''.join(c for c in map(chr, range(256)) if not c in keep_chars)
        self.translate = str.maketrans("", "", remove_chars)

    def getUrlTitles(self):
        pass

    def parseFile(self, content, title, url):
        """
        Add a file to the index.

        :param list content: A list of lowercase words from the file
        :param str title: The title of the document
        :param str url: The url of the page
        """
        content = content.lower()
        content = content.translate(self.translate)
        content = [word for word in content.split() if word not in stopwords]
        word_counter = Counter(content)

        i = len(self.urltitles)
        self.urltitles.append((url, title))

        for word, count in sorted(word_counter.items(), key=lambda x: x[1]):
            print(word, count)
            if count > 0:
                self.index[word].append((i, count))


def test():
    """
    Currently just a demonstration of doctest

    >>> test()
    True
    >>> test()
    False
    """
    return True


if __name__ == "__main__":
    doctest.testmod(verbose=True)
    test()
