import os
import json
import doctest
from collections import Counter
from nltk.corpus import stopwords
import re

stopwords = set(stopwords.words('english'))

# [(url, title), ...]
# {"word": [(index, freq), (index, freq), ...]}

class IndexGenerator:
    def __init__(self):
        self.urltitles = []
        self.index = {}

        keep_chars = ''.join(map(chr, range(ord('a'), ord('z') + 1))) + ' \n'
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
                pass


def test():
    """
    >>> test()
    True
    >>> test()
    False
    """
    return True


if __name__ == "__main__":
    doctest.testmod(verbose=True)
    test()