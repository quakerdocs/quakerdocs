import re
import nltk
import json
import string
import doctest
from nltk.corpus import stopwords
from collections import Counter, defaultdict
from nltk.stem.snowball import SnowballStemmer


try:
    stopwords = set(stopwords.words('english'))
except LookupError:
    nltk.download('stopwords')
    stopwords = set(stopwords.words('english'))


class IndexGenerator:
    def __init__(self):
        self.urltitles = []  # [(url, title), ...]
        self.index = defaultdict(list)  # {"word": [(index, freq), ...]}
        self.stemmer = SnowballStemmer(language="english").stem

        keep_chars = string.ascii_lowercase + string.digits + ' \n'
        remove_chars = ''.join(c for c in map(
            chr, range(256)) if not c in keep_chars)
        self.translate = str.maketrans("", "", remove_chars)

    def parse_file(self, content, title, url):
        """
        Add a file to the index.

        :param list content: A list of lowercase words from the file
        :param str title: The title of the document
        :param str url: The url of the page
        """
        content = content.lower()
        content = content.translate(self.translate)
        content = [self.stemmer(word)
                   for word in content.split() if word not in stopwords]
        word_counter = Counter(content)

        i = len(self.urltitles)
        self.urltitles.append((url, title))

        for word, count in sorted(word_counter.items(), key=lambda x: x[1]):
            self.index[word].append((i, count))

    def sort(self):
        """Sort the reversed index"""
        for key, value in self.index.items():
            self.index[key] = sorted(value, key=lambda x: -x[1])

    def to_json(self):
        """
        Return a json string containing the index and a mapping from ids to
        tuples of (url, title).
        """
        self.sort()
        return json.dumps(self.urltitles), json.dumps(self.index)


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
